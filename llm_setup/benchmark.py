import csv
import json
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

import psutil
import requests


# ============================================================
# CONFIG
# ============================================================

CONFIG_FILE = Path("config.json")


def load_config():
    """Load benchmark configuration from config.json."""

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {CONFIG_FILE}"
        )

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


config = load_config()

OLLAMA_URL = config["ollama_url"]
DEVICE = config["device"]
MODELS = config["models"]
PROMPT = config["prompt"]

BENCHMARK_CONFIG = config["benchmark"]
RESULT_CONFIG = config["results"]

MONITOR_INTERVAL = BENCHMARK_CONFIG["monitor_interval"]
REQUEST_TIMEOUT = BENCHMARK_CONFIG["request_timeout"]
KEEP_ALIVE = BENCHMARK_CONFIG["keep_alive"]

RESULTS_DIR = Path(
    RESULT_CONFIG["directory"]
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

CSV_FILE = (
    RESULTS_DIR /
    RESULT_CONFIG["csv"]
)

JSON_FILE = (
    RESULTS_DIR /
    RESULT_CONFIG["json"]
)


# ============================================================
# RAM
# ============================================================

def get_ram_usage():
    """Return system RAM information."""

    memory = psutil.virtual_memory()

    return {
        "used": memory.used,
        "available": memory.available,
        "total": memory.total,
        "percent": memory.percent,
    }


# ============================================================
# NVIDIA VRAM
# ============================================================

def get_nvidia_vram():
    """
    Read NVIDIA VRAM usage using nvidia-smi.
    """

    try:

        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu="
                "memory.used,memory.total",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=2,
        )

        if result.returncode != 0:
            return None

        gpus = []

        for line in result.stdout.strip().splitlines():

            if not line.strip():
                continue

            used, total = line.split(",")

            gpus.append(
                {
                    "used_mb": float(
                        used.strip()
                    ),
                    "total_mb": float(
                        total.strip()
                    ),
                }
            )

        return gpus

    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        ValueError,
    ):

        return None


# ============================================================
# AMD VRAM
# ============================================================

def get_amd_vram():
    """
    Try to read AMD VRAM using amd-smi.
    """

    try:

        result = subprocess.run(
            [
                "amd-smi",
                "metric",
                "--vram-usage",
                "--csv",
            ],
            capture_output=True,
            text=True,
            timeout=2,
        )

        if result.returncode != 0:
            return None

        return result.stdout.strip()

    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):

        return None


# ============================================================
# GPU
# ============================================================

def get_gpu_usage():
    """
    Detect NVIDIA or AMD GPU.
    """

    nvidia = get_nvidia_vram()

    if nvidia is not None:

        return {
            "vendor": "NVIDIA",
            "data": nvidia,
        }

    amd = get_amd_vram()

    if amd is not None:

        return {
            "vendor": "AMD",
            "data": amd,
        }

    return None


# ============================================================
# RESOURCE MONITOR
# ============================================================

class ResourceMonitor:

    def __init__(self, interval=0.1):

        self.interval = interval

        self.running = False
        self.thread = None

        self.ram_samples = []
        self.gpu_samples = []

    def start(self):

        self.running = True

        self.thread = threading.Thread(
            target=self._monitor,
            daemon=True,
        )

        self.thread.start()

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join()

    def _monitor(self):

        while self.running:

            # ----------------------------
            # RAM
            # ----------------------------

            ram = get_ram_usage()

            self.ram_samples.append(
                {
                    "timestamp": time.time(),
                    "used": ram["used"],
                    "percent": ram["percent"],
                }
            )

            # ----------------------------
            # GPU
            # ----------------------------

            gpu = get_gpu_usage()

            if gpu:

                self.gpu_samples.append(
                    {
                        "timestamp": time.time(),
                        "gpu": gpu,
                    }
                )

            time.sleep(self.interval)

    def get_results(self):

        result = {}

        # ----------------------------
        # RAM
        # ----------------------------

        if self.ram_samples:

            ram_values = [
                sample["used"]
                for sample in self.ram_samples
            ]

            result["ram"] = {
                "before": ram_values[0],
                "after": ram_values[-1],
                "peak": max(ram_values),
            }

        # ----------------------------
        # GPU
        # ----------------------------

        result["gpu_samples"] = (
            self.gpu_samples
        )

        return result


# ============================================================
# OLLAMA OPTIONS
# ============================================================

def get_ollama_options():
    """
    Build Ollama options based on config.json.
    """

    options = {}

    if DEVICE.lower() == "cpu":

        # Force CPU-only inference.
        options["num_gpu"] = 0

    elif DEVICE.lower() in (
        "auto",
        "gpu",
    ):

        # Let Ollama handle GPU offloading.
        #
        # We intentionally do not set num_gpu here.
        # Ollama will use its normal GPU behavior.

        pass

    else:

        raise ValueError(
            "device must be "
            "'cpu', 'gpu' or 'auto'"
        )

    return options


# ============================================================
# RUN MODEL
# ============================================================

def run_model(model, prompt):

    print()
    print("=" * 70)
    print(f"MODEL:  {model}")
    print(f"DEVICE: {DEVICE}")
    print("=" * 70)

    # ----------------------------------------
    # RAM before
    # ----------------------------------------

    ram_before = get_ram_usage()

    # ----------------------------------------
    # GPU before
    # ----------------------------------------

    gpu_before = get_gpu_usage()

    # ----------------------------------------
    # Resource monitor
    # ----------------------------------------

    monitor = ResourceMonitor(
        interval=MONITOR_INTERVAL
    )

    monitor.start()

    # ----------------------------------------
    # Ollama request
    # ----------------------------------------

    start_time = time.perf_counter()

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",

        json={
            "model": model,
            "prompt": prompt,

            "stream": False,

            "keep_alive": KEEP_ALIVE,

            "options": get_ollama_options(),
        },

        timeout=REQUEST_TIMEOUT,
    )

    end_time = time.perf_counter()

    monitor.stop()

    # ----------------------------------------
    # HTTP
    # ----------------------------------------

    response.raise_for_status()

    data = response.json()

    # ----------------------------------------
    # RAM after
    # ----------------------------------------

    ram_after = get_ram_usage()

    # ----------------------------------------
    # GPU after
    # ----------------------------------------

    gpu_after = get_gpu_usage()

    # ========================================================
    # Ollama metrics
    # ========================================================

    total_duration = data.get(
        "total_duration",
        0,
    )

    load_duration = data.get(
        "load_duration",
        0,
    )

    prompt_eval_count = data.get(
        "prompt_eval_count",
        0,
    )

    prompt_eval_duration = data.get(
        "prompt_eval_duration",
        0,
    )

    eval_count = data.get(
        "eval_count",
        0,
    )

    eval_duration = data.get(
        "eval_duration",
        0,
    )

    # ========================================================
    # Convert nanoseconds -> seconds
    # ========================================================

    total_seconds = (
        total_duration / 1e9
    )

    load_seconds = (
        load_duration / 1e9
    )

    prompt_seconds = (
        prompt_eval_duration / 1e9
    )

    generation_seconds = (
        eval_duration / 1e9
    )

    # ========================================================
    # Token speeds
    # ========================================================

    if prompt_seconds > 0:

        prompt_tokens_per_second = (
            prompt_eval_count /
            prompt_seconds
        )

    else:

        prompt_tokens_per_second = 0

    if generation_seconds > 0:

        generation_tokens_per_second = (
            eval_count /
            generation_seconds
        )

    else:

        generation_tokens_per_second = 0

    # ========================================================
    # Resource results
    # ========================================================

    resource_data = (
        monitor.get_results()
    )

    ram_data = resource_data.get(
        "ram",
        {},
    )

    gpu_samples = resource_data.get(
        "gpu_samples",
        [],
    )

    # ========================================================
    # GPU peak
    # ========================================================

    gpu_peak = calculate_gpu_peak(
        gpu_samples
    )

    # ========================================================
    # Result
    # ========================================================

    result = {

        "timestamp":
            datetime.now().isoformat(),

        "model":
            model,

        "device":
            DEVICE,

        # ------------------------------------
        # Timing
        # ------------------------------------

        "total_duration_s":
            total_seconds,

        "load_duration_s":
            load_seconds,

        "prompt_processing_s":
            prompt_seconds,

        "generation_s":
            generation_seconds,

        "python_wall_time_s":
            end_time - start_time,

        # ------------------------------------
        # Prompt
        # ------------------------------------

        "prompt_tokens":
            prompt_eval_count,

        "prompt_tokens_per_second":
            prompt_tokens_per_second,

        # ------------------------------------
        # Generation
        # ------------------------------------

        "output_tokens":
            eval_count,

        "generation_tokens_per_second":
            generation_tokens_per_second,

        # ------------------------------------
        # RAM
        # ------------------------------------

        "ram_before_gb":
            ram_before["used"] /
            1024**3,

        "ram_after_gb":
            ram_after["used"] /
            1024**3,

        "ram_peak_gb":
            ram_data.get(
                "peak",
                0,
            ) / 1024**3,

        # ------------------------------------
        # VRAM
        # ------------------------------------

        "gpu_before":
            gpu_before,

        "gpu_after":
            gpu_after,

        "gpu_peak":
            gpu_peak,

        # ------------------------------------
        # Response
        # ------------------------------------

        "response":
            data.get(
                "response",
                "",
            ),
    }

    return result


# ============================================================
# GPU PEAK
# ============================================================

def calculate_gpu_peak(samples):

    if not samples:
        return None

    latest_vendor = samples[-1]["gpu"]["vendor"]

    if latest_vendor == "NVIDIA":

        gpu_count = len(
            samples[-1]["gpu"]["data"]
        )

        peaks = []

        for gpu_index in range(gpu_count):

            values = []

            for sample in samples:

                gpus = sample["gpu"]["data"]

                if gpu_index < len(gpus):

                    values.append(
                        gpus[gpu_index][
                            "used_mb"
                        ]
                    )

            if values:

                peaks.append(
                    {
                        "gpu":
                            gpu_index,

                        "peak_used_mb":
                            max(values),
                    }
                )

        return {
            "vendor": "NVIDIA",
            "gpus": peaks,
        }

    # AMD output is currently kept as raw data.
    # amd-smi output differs between versions.

    if latest_vendor == "AMD":

        return {
            "vendor": "AMD",
            "raw_samples": [
                sample["gpu"]["data"]
                for sample in samples
            ],
        }

    return None


# ============================================================
# PRINT RESULT
# ============================================================

def print_result(result):

    print()

    print("Timing")
    print("-" * 45)

    print(
        f"Total:              "
        f"{result['total_duration_s']:.3f} s"
    )

    print(
        f"Model load:         "
        f"{result['load_duration_s']:.3f} s"
    )

    print(
        f"Prompt processing:  "
        f"{result['prompt_processing_s']:.3f} s"
    )

    print(
        f"Generation:         "
        f"{result['generation_s']:.3f} s"
    )

    print()

    print("Prompt")
    print("-" * 45)

    print(
        f"Tokens:             "
        f"{result['prompt_tokens']}"
    )

    print(
        f"Speed:              "
        f"{result['prompt_tokens_per_second']:.2f} tok/s"
    )

    print()

    print("Generation")
    print("-" * 45)

    print(
        f"Tokens:             "
        f"{result['output_tokens']}"
    )

    print(
        f"Speed:              "
        f"{result['generation_tokens_per_second']:.2f} tok/s"
    )

    print()

    print("RAM")
    print("-" * 45)

    print(
        f"Before:             "
        f"{result['ram_before_gb']:.2f} GB"
    )

    print(
        f"After:              "
        f"{result['ram_after_gb']:.2f} GB"
    )

    print(
        f"Peak:               "
        f"{result['ram_peak_gb']:.2f} GB"
    )

    print()

    print("VRAM")
    print("-" * 45)

    print(
        f"Before:             "
        f"{format_gpu(result['gpu_before'])}"
    )

    print(
        f"After:              "
        f"{format_gpu(result['gpu_after'])}"
    )

    print(
        f"Peak:               "
        f"{format_gpu(result['gpu_peak'])}"
    )


# ============================================================
# FORMAT GPU
# ============================================================

def format_gpu(gpu):

    if gpu is None:
        return "N/A"

    if isinstance(gpu, dict):

        vendor = gpu.get(
            "vendor",
            "Unknown",
        )

        if vendor == "NVIDIA":

            values = []

            for item in gpu["data"]:

                values.append(
                    f"{item['used_mb']:.0f} MB"
                )

            return (
                "NVIDIA: " +
                ", ".join(values)
            )

        return f"{vendor}"

    return str(gpu)


# ============================================================
# SAVE JSON
# ============================================================

def save_json(results):

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False,
        )


# ============================================================
# SAVE CSV
# ============================================================

def save_csv(results):

    if not results:
        return

    fields = [

        "timestamp",
        "model",
        "device",

        "total_duration_s",
        "load_duration_s",

        "prompt_processing_s",
        "prompt_tokens",
        "prompt_tokens_per_second",

        "generation_s",
        "output_tokens",
        "generation_tokens_per_second",

        "ram_before_gb",
        "ram_after_gb",
        "ram_peak_gb",

        "python_wall_time_s",
    ]

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        writer.writeheader()

        for result in results:

            writer.writerow(
                {
                    field:
                        result.get(field)
                    for field in fields
                }
            )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("OLLAMA MODEL BENCHMARK")
    print("=" * 70)

    print(
        f"Ollama URL: {OLLAMA_URL}"
    )

    print(
        f"Device:     {DEVICE}"
    )

    print()

    print("Models:")

    for model in MODELS:

        print(
            f"  - {model}"
        )

    print()

    results = []

    for model in MODELS:

        try:

            result = run_model(
                model,
                PROMPT,
            )

            results.append(
                result
            )

            print_result(
                result
            )

        except Exception as error:

            print()

            print(
                f"ERROR running {model}"
            )

            print(error)

    # ----------------------------------------
    # Save
    # ----------------------------------------

    save_json(results)

    save_csv(results)

    print()

    print("=" * 70)

    print("Benchmark finished.")

    print()

    print(
        f"CSV:  {CSV_FILE}"
    )

    print(
        f"JSON: {JSON_FILE}"
    )


if __name__ == "__main__":

    main()
