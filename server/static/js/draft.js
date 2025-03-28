function resizeCanvas(canvas) {
    const outerCanvasContainer = document.getElementById('fabric-canvas-wrapper');

    if (!outerCanvasContainer || !canvas) return;
    const containerWidth = outerCanvasContainer.clientWidth;
    const scale = containerWidth / canvas.getWidth();
    const zoom = canvas.getZoom() * scale;

    canvas.setDimensions({width: containerWidth});
    canvas.setViewportTransform([zoom, 0, 0, zoom, 0, 0]);
}

if ($) {
    const $ = (id) => document.getElementById(id);

    const canvas = new fabric.Canvas('drawingCanvas', {
        isDrawingMode: true,
        width: 1105,
        height: 880
    });

    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);

    fabric.Object.prototype.transparentCorners = false;

    var drawingModeEl = $('drawing-mode'),
        drawingOptionsEl = $('drawing-mode-options'),
        drawingColorEl = $('drawing-color'),
        drawingShadowColorEl = $('drawing-shadow-color'),
        drawingLineWidthEl = $('drawing-line-width'),
        drawingShadowWidth = $('drawing-shadow-width'),
        drawingShadowOffset = $('drawing-shadow-offset'),
        clearEl = $('clear-canvas');

    clearEl.onclick = function () {
        canvas.clear();
    };

    drawingModeEl.onclick = function () {
        canvas.isDrawingMode = !canvas.isDrawingMode;
        drawingModeEl.innerHTML = canvas.isDrawingMode ? 'Cancel drawing mode' : 'Enter drawing mode';
    };

    if (fabric.PatternBrush) {
        var vLinePatternBrush = new fabric.PatternBrush(canvas);
        vLinePatternBrush.getPatternSrc = function () {
            var patternCanvas = document.createElement('canvas');
            patternCanvas.width = patternCanvas.height = 10;
            var ctx = patternCanvas.getContext('2d');
            ctx.strokeStyle = this.color;
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(0, 5);
            ctx.lineTo(10, 5);
            ctx.closePath();
            ctx.stroke();
            return patternCanvas;
        };

        var hLinePatternBrush = new fabric.PatternBrush(canvas);
        hLinePatternBrush.getPatternSrc = function () {
            var patternCanvas = document.createElement('canvas');
            patternCanvas.width = patternCanvas.height = 10;
            var ctx = patternCanvas.getContext('2d');
            ctx.strokeStyle = this.color;
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(5, 0);
            ctx.lineTo(5, 10);
            ctx.closePath();
            ctx.stroke();
            return patternCanvas;
        };
    }

    $('drawing-mode-selector').onchange = function () {
        let selectedBrush = this.value;
        let brushes = {
            "hline": vLinePatternBrush,
            "vline": hLinePatternBrush,
            "pencil": new fabric.PencilBrush(canvas)
        };

        canvas.freeDrawingBrush = brushes[selectedBrush] || new fabric.PencilBrush(canvas);
        if (canvas.freeDrawingBrush) {
            canvas.freeDrawingBrush.color = drawingColorEl.value;
            canvas.freeDrawingBrush.width = parseInt(drawingLineWidthEl.value, 10) || 1;
            canvas.freeDrawingBrush.shadow = new fabric.Shadow({
                blur: parseInt(drawingShadowWidth.value, 10) || 0,
                color: drawingShadowColorEl.value,
                affectStroke: true
            });
        }
    };

    drawingColorEl.onchange = function () {
        if (canvas.freeDrawingBrush) canvas.freeDrawingBrush.color = this.value;
    };

    drawingLineWidthEl.onchange = function () {
        if (canvas.freeDrawingBrush) canvas.freeDrawingBrush.width = parseInt(this.value, 10) || 1;
    };

    window.addEventListener("resize", function () {
        resizeCanvas(canvas);
    });

    setTimeout(() => {
        let id_description = document.getElementById('id_description');
        if (id_description) {
            canvas.setDimensions({width: id_description.clientWidth})
        }
    }, 300);

}
