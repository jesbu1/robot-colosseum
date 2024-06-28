from setuptools import setup

setup(
    package_data={
        "colosseum": [
            "rlbench/task_ttms/*.ttm",
            "assets/textures/*.jpg",
            "assets/textures/*.png",
            "assets/models/*.ttm",
            "assets/configs/*.yaml",
        ],
    },
    entry_points={
        "console_scripts": [
            "task_builder=colosseum.tools.task_builder:main",
            "collect_demo=colosseum.tools.collect_demo:main",
            "visualize_task=colosseum.tools.visualize_task:main",
            "dataset_generator=colosseum.tools.dataset_generator:main",
        ]
    },
)
