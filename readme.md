# Gradient

Gradient is a node based editor for use with Autodesk Fusion 360. I started working on Gradient because I wanted a tool for myself and others to make useful, fun, interesting and weird 3D models with. 3D models that are not easily made with the Fusion 360's vanilla design tools.

![screenshot0](samples/Rand_boxes_sample_3d.png)

![screenshot1](samples/Rand_boxes_sample_gui.png)

Gradients intent is to allow you to make algorithemically defined geometry that would be tricky to make with the standard Fusion parametric or direct design tools. Gradient will also provide a quicker and more designer friendly way to leverage the Fusion 360 API. The intent behind this is to allow for others to extend the CAD systems capabilities by making analysis tools, CAM tools and anything else you may need without the difficulties of coding a full addin.

## 🚧Warning!🚧

Gradient is currently in a very early state. What that means is that a tiny fraction of the functionality I'd like to eventually add has been implemented and there will be some bugs and general jankyness.

## Installation

In theory Gradient should be compatible on all windows and mac computers that can run Fusion 360. In practice this code has only been tested to run on my personal windows pc. If you encounter difficulties installing / running Gradient please open an issue.

### Windows Installation:

Clone the Gradient repository to the following path: 

```
C:\Users\user_name\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\Gradient
```

After cloning the repository run the following command to install dependencies:

```
pip install -r C:\Users\Dylan Rice\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\Gradient\modules\requirements.txt
```

Once dependencies are installed you can run Gradient from the Scripts and Add-Ins menu in Fusion 360.
