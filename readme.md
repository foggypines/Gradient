This is Gradient. A node based editor for use with Autodesk Fusion 360. Gradient is currently in a very, very early state. What that means is that a tiny fraction of the functionality I'd like to eventually implement is here with a large amount of bugs and issues.

I made Gradient because I wanted a tool for myself and others to make useful, fun, interesting and weird things. Things that you may not always be able to easily make with the Fusion 360 design tools in there vanilla state.

My plan for Gradient is not to re-implement the entire Fusion 360 API with nodes but to create an interface that minimally talks to the Fusion 360 application. This will enable Gradient to primarily operate in it's own thread and leverage other commonly used python libraries like numpy and scipy.