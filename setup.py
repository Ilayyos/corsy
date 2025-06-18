from setuptools import setup, find_packages

setup(
    name="corsy",
    version="0.2.0",
    description="CORS Misconfiguration Scanner",
    author="Somdev Sangwan",
    license="MIT",
    packages=find_packages(),
    py_modules=["corsy"],
    include_package_data=True,
    package_data={"db": ["details.json"]},
    install_requires=["requests"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["corsy=corsy:main"],
    },
)
