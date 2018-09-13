catkin_tools_document
=====================

This package is an experimental documentation-builder for ROS packages, similar to
[rosdoc_lite](http://wiki.ros.org/rosdoc_lite). It differs in the following ways:

- It's implemented as a `catkin_tools` plugin, so it fits naturally into the
  developer workflow, and piggy-backs off that package's capabilities as far as
  package discovery, dependency resolution, and parallel execution.
- Because it operates at the workspace level rather than package-by-package, it
  automatically handles linking up doxygen between dependent packages.
- It automatically links to [cppreference](http://en.cppreference.com/w/) for
  standard library functions and headers.
- It double-builds for doxygen, once without links to get the XML output of
  in-package symbols only, and once with all links to get the HTML output. This
  avoids the duplicate symbol warnings which rosdoc_lite produces.

Demonstration
-------------

Using a virtualenv is recommended if using `pip`. Alternatively, you can get a
system package for Ubuntu or Debian [on my PPA][1].

```
pip install catkin_tools_document
mkdir -p catkin_ws/src && cd catkin_ws
rosinstall_generator ros_base --deps --tar --rosdistro indigo > src/.rosinstall
wstool up -t src
catkin document
```

Now open up `catkin_ws/docs/index.html` in the browser of your choice.

[1]: https://launchpad.net/~mikepurvis/+archive/ubuntu/catkin

Release
-------

```
# Upload to pypi
python setup.py sdist bdist_wheel
twine upload dist/*

# Upload to launchpad. Need to rebuild with signing as the built-in capability in stdeb
# isn't released yet, and I couldn't get dpkg-sig to work either for a post-build signature.
python setup.py --command-packages=stdeb.command sdist_dsc --upstream-version-suffix=xenial --suite xenial
cd deb_dist/*
dpkg-buildpackage -S
dput ppa:mikepurvis/catkin ../*_source.changes
```
