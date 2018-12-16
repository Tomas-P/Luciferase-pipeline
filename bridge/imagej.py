from jbridge import jnius

String = jnius.autoclass("java.lang.String")

# nested class structure reflecting structure of ImageJ2 classes
# sparse because only the classes actually needed have been aquired
# add classes as needed
class net:

    class imagej:
        ImageJ = jnius.autoclass("net.imagej.ImageJ")

        class legacy:
            LegacyService = jnius.autoclass('net.imagej.legacy.LegacyService')

# There must be a net.imagej.ImageJ instance in order for some items
# to work properly
imagej = net.imagej.ImageJ()

# nested class structure reflecting structure of ImageJ1 classes
# not all defined because only needed classes have been aquired
# add classes as needed
class ij:
    
    IJ = jnius.autoclass('ij.IJ')

    ImagePlus = jnius.autoclass('ij.ImagePlus')

    WindowManager = jnius.autoclass('ij.WindowManager')

    Prefs = jnius.autoclass("ij.Prefs")

    Macro = jnius.autoclass('ij.Macro')

    Menus = jnius.autoclass('ij.Menus')

    class gui:

        PolygonRoi = jnius.autoclass("ij.gui.PolygonRoi")

        GenericDialog = jnius.autoclass('ij.gui.GenericDialog')

    class measure:

        ResultsTable = jnius.autoclass('ij.measure.ResultsTable')

    class process:

        FloatProcessor = jnius.autoclass('ij.process.FloatProcessor')

        ImageProcessor = jnius.autoclass('ij.process.ImageProcessor')

    class plugin:

        Duplicator = jnius.autoclass('ij.plugin.Duplicator')

        ContrastEnhancer = jnius.autoclass('ij.plugin.ContrastEnhancer')

        ImageCalculator = jnius.autoclass('ij.plugin.ImageCalculator')

        FolderOpener = jnius.autoclass('ij.plugin.FolderOpener')

        class frame:

            RoiManager = jnius.autoclass('ij.plugin.frame.RoiManager')

        class filter:

            RankFilters = jnius.autoclass('ij.plugin.filter.RankFilters')

            BackgroundSubtracter = jnius.autoclass('ij.plugin.filter.BackgroundSubtracter')

            PlugInFilter = jnius.autoclass('ij.plugin.filter.PlugInFilter')

    class macro:

        Debugger = jnius.autoclass('ij.macro.Debugger')

        MacroConstants = jnius.autoclass('ij.macro.MacroConstants')

        MacroExtension = jnius.autoclass('ij.macro.MacroExtension')

        ExtensionDescriptor = jnius.autoclass('ij.macro.FunctionFinder')

        Functions = jnius.autoclass('ij.macro.Functions')

        Interpreter = jnius.autoclass('ij.macro.Interpreter')

        MacroRunner = jnius.autoclass('ij.macro.MacroRunner')

        StartupRunner = jnius.autoclass('ij.macro.StartupRunner')

        Symbol = jnius.autoclass('ij.macro.Symbol')

        Tokenizer = jnius.autoclass('ij.macro.Tokenizer')

        Variable = jnius.autoclass('ij.macro.Variable')

    class util:

        Tools = jnius.autoclass('ij.util.Tools')


# Fiji classes that do not have an owning package
# these are items I want to use
#----------------------------------------------
RATSQuadtree = jnius.autoclass('RATSQuadtree')
RATS_ = jnius.autoclass('RATS_')
SIFT_Align = jnius.autoclass('SIFT_Align')
        
            


def open_image(filename :str) -> ij.ImagePlus:
    # open an image file as an ij.ImagePlus
    filename = String(filename)
    return ij.ImagePlus(filename)

def open_stack(foldername :str) -> ij.ImagePlus:
    # open an image series as a stack
    name = String(foldername)
    return ij.plugin.FolderOpener.open(name)

def ij_run(image :ij.ImagePlus, arg1 :str, arg2 :str):
    arg1 = String(arg1)
    arg2 = String(arg2)
    ij.IJ.run(image,arg1,arg2)

def initial_filters(stack):
    ij_run(stack, "Enhance Contrast...", "saturated=0.3 equalize process_all")
    ij_run(stack, "Median...", "radius=2 stack")
    ij_run(stack, "Subtract Background...", "rolling=50 stack")

def align(stack):
    stack.show()
    sifter = SIFT_Align()
    sifter.run(String(""))
    aligned = ij.WindowManager.getCurrentImage()
    aligned.hide()
    stack.hide()
    ij.WindowManager.getAllNonImageWindows()[0].hide()
    return aligned

def make_mask(image :ij.ImagePlus) -> ij.ImagePlus:
    ij_run(image, "Enhance Contrast...", "saturated=0.3 equalize")
    ij_run(image, "Median...", "radius=2")
    ij_run(image, "Subtract Background...", "rolling=50")
    # use the RATS_ class to create a mask from an image
    ij.Macro.setOptions(
        String("noise=25 lambda=3 min=40")
        )
    ratter = RATS_()
    ratter.setup(String(""), image)
    processor = image.getProcessor()
    ratter.run(processor)
    mask = ij.WindowManager.getCurrentImage()
    mask.hide()
    ij_run(mask, "Erode", "")
    ij_run(mask, "16-bit", "")
    # 255 * 257 == 65535 == (2 ** 16) - 1
    ij_run(mask, "Multiply...", "value=257")
    # remove some of the noise
    ij_run(mask, "Median...", "radius=2")
    return mask

def apply_mask(stack, mask):
    ic = ij.plugin.ImageCalculator()
    return ic.run(String("AND create stack"), stack, mask)

def filtering(foldername,imagename):
    stack = open_stack(foldername)
    image = open_image(imagename)
    mask = make_mask(image)
    initial_filters(stack)
    aligned = align(stack)
    masked = apply_mask(aligned, mask)
    return masked
