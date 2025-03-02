Gradient is a node based editor for use with Autodesk Fusion 360. I started working on Gradient because I wanted a tool for myself and others to make useful, fun, interesting and weird things. Things that you may not always be able to easily make with the Fusion 360 design tools in there vanilla state.

Gradients intent is to allow you to make algorithemically defined geometry that would be tricky to make with the standard Fusion parametric or direct design tools. Gradient will also provide a quicker and more designer friendly way to leverage the Fusion 360 API. The intent behind this is to allow for others to extend the CAD systems capabilities by making analysis tools, CAM tools and anything else you may need without the difficulties of coding a python or C++ addin.

🚧Warning!🚧

Gradient is currently in a very early state. What that means is that a tiny fraction of the functionality has been implemented and there will be some bugs and general jankyness.

My plan for Gradient is not to re-implement the entire Fusion 360 API with nodes but to create an interface that minimally talks to the Fusion 360 application. This will enable Gradient to primarily operate in it's own thread and leverage other commonly used python libraries like numpy and scipy.