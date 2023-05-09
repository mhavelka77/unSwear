
<a name="readme-top"></a>





<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="">
    <img src="holdmysnail.png" alt="Logo">
  </a>

<h2 align="center">unSwear</h3>

  <p align="center">
    Fixing Toxicity by replacing curse words!
    <br />
    <br />
  </p>
</div>


## About The Project

This repo contains a simple python script that listens for words and then replaces them based on the file `replacements.csv`.

You can add new words here, separated by comma.



## How to set up?

The setup should be as simple as:

```bash
python -m pip install -r requirements.txt
```

and

```bash
python unswear.py
```

## Executable for windows

If you want to run this on windows without Python, navigate to `dist` folder and run the pre-compiled `Unswear.exe`

**NOTE:** The application will open as a tray icon on the bottom-right side of the taskbar.
The executable will use the other `replacements.csv` file present in the same folder as the executable. **You should only keep the `dist` folder if you need just the executable.**