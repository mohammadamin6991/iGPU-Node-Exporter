# Usage example: python3 igpu_exporter.py 9101 http://localhost:9101/metrics

from prometheus_client import start_http_server, Metric, REGISTRY
import sys
import time
import subprocess

class DataCollector(object):
    def __init__(self, endpoint):
        self._endpoint = endpoint

    def collect(self):
        # Fetch the data
        cmd = "/usr/bin/timeout -k 3 3 /usr/bin/intel_gpu_top -J"
        process = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        igpu = process.stdout.decode('utf-8')

        # Helper function to safely extract values
        def extract_value(data, start, end):
            try:
                return data.split(start)[2].split(end)[0]
            except IndexError:  # If the split does not find the pattern and thus no index 2
                return '0'  # Return '0' or some default value indicating no data

        # Video busy utilisation
        try:
            video_busy = igpu.split('engines')[3].split('"Video/0": {\n\t\t\t"busy": ')[1].split(',')[0]
        except IndexError:
            video_busy = '0'  # Default value if not found
        metric = Metric('igpu_video_busy', 'Video busy utilisation in %', 'summary')
        metric.add_sample('igpu_video_busy', value=video_busy, labels={})
        yield metric

        # Render busy utilisation
        try:
            render_busy = igpu.split('engines')[3].split('"Render/3D/0": {\n\t\t\t"busy": ')[1].split(',')[0]
        except IndexError:
            render_busy = '0'  # Default value if not found
        metric = Metric('igpu_render_busy', 'Render busy utilisation in %', 'summary')
        metric.add_sample('igpu_render_busy', value=render_busy, labels={})
        yield metric

        # Enhance busy utilisation
        try:
            enhance_busy = igpu.split('engines')[3].split('"VideoEnhance/0": {\n\t\t\t"busy": ')[1].split(',')[0]
        except IndexError:
            enhance_busy = '0'  # Default value if not found
        metric = Metric('igpu_enhance_busy', 'Enhance busy utilisation in %', 'summary')
        metric.add_sample('igpu_enhance_busy', value=enhance_busy, labels={})
        yield metric

        # Power utilisation
        power = extract_value(igpu, '"power": {\n\t\t"value": ', ',')
        metric = Metric('igpu_power', 'Power utilisation in W', 'summary')
        metric.add_sample('igpu_power', value=power, labels={})
        yield metric


if __name__ == '__main__':
    start_http_server(int(sys.argv[1]))
    REGISTRY.register(DataCollector(sys.argv[2]))

    while True: time.sleep(1)
