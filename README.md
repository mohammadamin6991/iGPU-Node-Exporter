gra# iGPU-Node-Exporter
A Python based node, exporting Intel iGPU data for Prometheus.

This has been made & tested on a Intel Xeon E3-1275v6 CPU.


## Requirements
### Apt packages
 - python3
 - python3-pip
 - intel_gpu_too

### Pip packages
 - prometheus_client
 - subprocess

## Usage
### iGPU host
Syntax: `python3 script.py port http_service_metric_point`

Real use case example: `python3 igpu_exporter.py 9101 http://localhost:9101/metrics`

1. Install python3-venv and create a virtual environment for this porject `python3 -m venv /path/to/venv`
2. Install requierd packages into this env
   ```shell
   source /path/to/venv/bin/activate
   pip instal prometheus_client
   ```
3. Add the service file to `/etc/systemd/system/`. change value of the variable to meet your needs
4. Test the service with `systemctl daemon-reload && systemctl start igpu_exporter.service`
5. Check the status with `systemctl status igpu_exporter.service`
6. Add the service to run at boot with `systemctl enable igpu_exporter.service`

#### Metric End Point data
```
# HELP igpu_video_busy  Video busy utilisation in %
# TYPE igpu_video_busy summary
igpu_video_busy 0.0
# HELP igpu_render_busy Render busy utilisation in %
# TYPE igpu_render_busy summary
igpu_render_busy 0.0
# HELP igpu_enhance_busy Enhance busy utilisation in %
# TYPE igpu_enhance_busy summary
igpu_enhance_busy 0.0
# HELP igpu_power Power utilisation in W
# TYPE igpu_power summary
igpu_power 0.0
```

### Prometheus configuration
Please see `prometheus.yml`

## Required changes for you
 - Adapt path to script in `igpu_exporter.service`
 - Adapt http_service_metric_point in `igpu_exporter.service`
 - Adapt the target in `prometheus.yml`
