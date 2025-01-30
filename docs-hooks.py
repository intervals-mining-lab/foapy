import os
import shutil


def on_post_build(config, **kwargs):
    copy_benchmarks_report(config)


def on_serve(server, config, builder, **kwargs):
    copy_benchmarks_report(config)


def copy_benchmarks_report(config):
    destination = os.path.join(
        config["site_dir"], "development", "benchmarks", "report"
    )
    if os.path.exists("benchmarks/html"):
        shutil.rmtree(destination) if os.path.exists(destination) else None
        shutil.copytree("benchmarks/html", destination)
    else:
        print("No benchmarks/html directory found")
