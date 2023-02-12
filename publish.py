def setup():
    import os
    
    print("installing modules...")
    cmds = [
        "pip install setuptools",
        "pip install twine",
        "pip install wheel",
        "python3 setup.py sdist bdist_wheel",
    ]
    for i in cmds:
        os.system(i)

    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nLogin:")
    os.system("python3 -m twine upload --repository pypi dist/*")
  
input("[ENTER]")

setup()
