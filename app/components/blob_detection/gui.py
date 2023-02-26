"""GUI for adjusting blob detection parameters."""

import tkinter as tk
from app.components.blob_detection import BlobDetection
from app.components.tkinter_gui import GUI, TkVar
from app.components.tkinter_gui.components import HorizontalSlider, Checkbox


class BlobDetectionGUI(GUI):
    """GUI for adjusting the blob detection parameters."""
    blob_detection: BlobDetection

    def __init__(self, blob_detection: BlobDetection) -> None:
        """Create new blob detection GUI."""
        # Instantiate GUI
        super().__init__(
            'Configure blob detection',
            width=560,
            height=600
        )

        self.blob_detection = blob_detection

        # Set blob detection parameters
        params = blob_detection.params

        ###############
        # Compose GIU #
        ###############

        # How to configure a GUI element:
        #
        # Declare a traced tkinter Var:
        # Assign it to `frame` and set the parameter attribute as the name and the parameter value as the value.
        # Add tracing using the `trace_var` convenience function.
        #
        # Create the GIU element and pass the variable parameter.
        #
        # Pack the GUI element.

        #################
        # Color channel #
        #################

        # Extract color channel
        extractColorChannel = tk.BooleanVar(
            self.frame,
            name='extractColorChannel',
            value=params.extractColorChannel
        )
        self.trace_var(extractColorChannel)
        chanCheckbox = Checkbox(
            self.frame,
            label='extractColorChannel',
            variable=extractColorChannel
        )
        chanCheckbox.pack()
        # Color channel radio buttons
        colorChannel = tk.StringVar(
            self.frame,
            name='colorChannel',
            value=params.colorChannel
        )
        self.trace_var(colorChannel)
        rButton = tk.Radiobutton(
            self.frame,
            text='R',
            value='r',
            variable=colorChannel
        )
        gButton = tk.Radiobutton(
            self.frame,
            text='G',
            value='g',
            variable=colorChannel
        )
        bButton = tk.Radiobutton(
            self.frame,
            text='B',
            value='b',
            variable=colorChannel
        )
        rButton.pack()
        gButton.pack()
        bButton.pack()

        ########
        # Blur #
        ########

        # Use blurring filter
        useBlur = tk.BooleanVar(
            self.frame,
            name='useBlur',
            value=params.useBlur
        )
        self.trace_var(useBlur)
        useBCheckbox = Checkbox(
            self.frame,
            label='useBlur',
            variable=useBlur
        )
        useBCheckbox.pack()
        # Blur amount
        blurAmount = tk.IntVar(
            self.frame,
            name='blurAmount',
            value=params.blurAmount
        )
        self.trace_var(blurAmount)
        bAmountSlider = HorizontalSlider(
            self.frame,
            label='blurAmount',
            from_=2,
            to=200,
            resolution=1,
            variable=blurAmount
        )
        bAmountSlider.pack()

        #########
        # Color #
        #########

        # Filter by color
        filterByColor = tk.BooleanVar(
            self.frame,
            name='filterByColor',
            value=params.filterByColor
        )
        self.trace_var(filterByColor)
        filterColCheckbox = Checkbox(
            self.frame,
            label='filterByColor',
            variable=filterByColor
        )
        filterColCheckbox.pack()
        # Blob color
        blobColor = tk.IntVar(
            self.frame,
            name='blobColor',
            value=params.blobColor
        )
        self.trace_var(blobColor)
        bColSlider = HorizontalSlider(
            self.frame,
            label='blobColor',
            from_=0,
            to=255,
            resolution=1,
            variable=blobColor
        )
        bColSlider.pack()

        ##############
        # Thresholds #
        ##############

        # Binary thresholds checkbox
        useBinaryThresholds = tk.BooleanVar(
            self.frame,
            name='useBinaryThresholds',
            value=params.useBinaryThresholds
        )
        self.trace_var(useBinaryThresholds)
        binaryTCheckbox = Checkbox(
            self.frame,
            label='useBinaryThresholds',
            variable=useBinaryThresholds
        )
        binaryTCheckbox.pack()
        # Min threshold slider
        minThreshold = tk.IntVar(
            self.frame,
            name='minThreshold',
            value=params.minThreshold
        )
        self.trace_var(minThreshold)
        minTSlider = HorizontalSlider(
            self.frame,
            label='minThreshold',
            from_=0,
            to=255,
            resolution=1,
            variable=minThreshold
        )
        minTSlider.pack()
        # Max threshold slider
        maxThreshold = tk.IntVar(
            self.frame,
            value=params.maxThreshold,
            name='maxThreshold'
        )
        self.trace_var(maxThreshold)
        maxTSlider = HorizontalSlider(
            self.frame,
            label='maxThreshold',
            from_=0,
            to=255,
            resolution=1,
            variable=maxThreshold
        )
        maxTSlider.pack()

        ########
        # Area #
        ########

        # Filter by area checkbox
        filterByArea = tk.BooleanVar(
            self.frame,
            name='filterByArea',
            value=params.filterByArea
        )
        self.trace_var(filterByArea)
        filterACheckbox = Checkbox(
            self.frame,
            label='filterByArea',
            variable=filterByArea
        )
        filterACheckbox.pack()
        # Min area slider
        minArea = tk.DoubleVar(
            self.frame,
            name='minArea',
            value=params.minArea
        )
        self.trace_var(minArea)
        minASlider = HorizontalSlider(
            self.frame,
            label='minArea',
            from_=1,
            to=10_000,
            resolution=1,
            variable=minArea
        )
        minASlider.pack()
        # Max area slider
        maxArea = tk.DoubleVar(
            self.frame,
            name='maxArea',
            value=params.maxArea
        )
        self.trace_var(maxArea)
        maxASlider = HorizontalSlider(
            self.frame,
            label='maxArea',
            from_=2_500,
            to=100_000,
            resolution=1,
            variable=maxArea
        )
        maxASlider.pack()

        ###############
        # Circularity #
        ###############

        # Filter by circularity
        filterByCircularity = tk.BooleanVar(
            self.frame,
            name='filterByCircularity',
            value=params.filterByCircularity
        )
        self.trace_var(filterByCircularity)
        filterCircCheckbox = Checkbox(
            self.frame,
            label='filterByCircularity',
            variable=filterByCircularity
        )
        filterCircCheckbox.pack()
        # Min circularity slider
        minCircularity = tk.DoubleVar(
            self.frame,
            name='minCircularity',
            value=params.minCircularity
        )
        self.trace_var(minCircularity)
        minCircSlider = HorizontalSlider(
            self.frame,
            label='minCircularity',
            from_=0.1,
            to=1,
            resolution=0.1,
            variable=minCircularity
        )
        minCircSlider.pack()
        # Max circularity slider
        maxCircularity = tk.DoubleVar(
            self.frame,
            name='maxCircularity',
            value=params.maxCircularity
        )
        self.trace_var(maxCircularity)
        maxCircSlider = HorizontalSlider(
            self.frame,
            label='maxCircularity',
            from_=0.1,
            to=1,
            resolution=0.1,
            variable=maxCircularity
        )
        maxCircSlider.pack()

        #############
        # Convexity #
        #############

        # Filter by convexity
        filterByConvexity = tk.BooleanVar(
            self.frame,
            name='filterByConvexity',
            value=params.filterByConvexity
        )
        self.trace_var(filterByConvexity)
        filterConvCheckbox = Checkbox(
            self.frame,
            label='filterByConvexity',
            variable=filterByConvexity
        )
        filterConvCheckbox.pack()
        # Min convexity slider
        minConvexity = tk.DoubleVar(
            self.frame,
            name='minConvexity',
            value=params.minConvexity
        )
        self.trace_var(minConvexity)
        minConvSlider = HorizontalSlider(
            self.frame,
            label='minConvexity',
            from_=0.1,
            to=1,
            resolution=0.1,
            variable=minConvexity
        )
        minConvSlider.pack()
        # Max convexity slider
        maxConvexity = tk.DoubleVar(
            self.frame,
            name='maxConvexity',
            value=params.maxConvexity
        )
        self.trace_var(maxConvexity)
        maxConvSlider = HorizontalSlider(
            self.frame,
            label='maxConvexity',
            from_=0.1,
            to=1,
            resolution=0.1,
            variable=maxConvexity
        )
        maxConvSlider.pack()

        ###########
        # Inertia #
        ###########

        # Filter by inertia
        filterByInertia = tk.BooleanVar(
            self.frame,
            name='filterByInertia',
            value=params.filterByInertia
        )
        self.trace_var(filterByInertia)
        filterInCheckbox = Checkbox(
            self.frame,
            label='filterByInertia',
            variable=filterByInertia
        )
        filterInCheckbox.pack()
        # Min inertia slider
        minInertiaRatio = tk.DoubleVar(
            self.frame,
            name='minInertiaRatio',
            value=params.minInertiaRatio
        )
        self.trace_var(minInertiaRatio)
        minInSlider = HorizontalSlider(
            self.frame,
            label='minInertiaRatio',
            from_=0.1,
            to=1,
            resolution=0.1,
            variable=minInertiaRatio
        )
        minInSlider.pack()
        # Max inertia slider
        maxInertiaRatio = tk.DoubleVar(
            self.frame,
            name='maxInertiaRatio',
            value=params.maxInertiaRatio
        )
        self.trace_var(maxInertiaRatio)
        maxInSlider = HorizontalSlider(
            self.frame,
            label='maxInertiaRatio',
            from_=0.1,
            to=1,
            resolution=0.1,
            variable=maxInertiaRatio
        )
        maxInSlider.pack()

        ##########################
        # Distance between blobs #
        ##########################

        # Min distance between blobs
        minDistBetweenBlobs = tk.DoubleVar(
            self.frame,
            name='minDistBetweenBlobs',
            value=params.minDistBetweenBlobs
        )
        self.trace_var(minDistBetweenBlobs)
        minDistSlider = HorizontalSlider(
            self.frame,
            label='minDistBetweenBlobs',
            from_=0,
            to=2_000,
            resolution=1,
            variable=minDistBetweenBlobs
        )
        minDistSlider.pack()

        ################
        # Write button #
        ################
        writeButton = tk.Button(
            self.frame,
            text='Write parameters to cache.',
            command=self.blob_detection.params.__write_parameters__
        )
        writeButton.pack()

    def trace_callback(self, var: TkVar, name: str, index: str, mode: str) -> None:
        """Update blob detection parameters on Var trace."""
        # Update the traced parameter
        val = var.get()
        self.blob_detection.update_parameter(name, val)
