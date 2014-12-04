screenStitch
============

Will ask for files, find the region that changed between first two files, crop the changes, and stitch a final image together. Outputs a new stitch.png in the directory of first selected image and will overwrite any existing files with same name.

***

Works best with images that are *exactly* the same, except for the regions that should be stitched. At least one horizontal line has to be similar between two changed regions. For example, multiple screenshots of a window can be taken. The only difference being that one pane is scrolled down. screenStitch will then make a long screenshot of the scrollable section.

***

Licensed under the MIT license (http://opensource.org/licenses/MIT)

If you make any changes or use this in a project, I would appreciate if you tell me. Please leave this notice intact.
