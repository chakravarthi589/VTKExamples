#!/usr/bin/env python

import vtk


def main():
    colors = vtk.vtkNamedColors()

    # Create a rendering window and renderer.
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.SetWindowName("Cube")
    renWin.AddRenderer(ren)

    # Create a renderwindowinteractor.
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Create cube.
    cube = vtk.vtkCubeSource()
    cube.Update()

    # mapper
    cubeMapper = vtk.vtkPolyDataMapper()
    cubeMapper.SetInputData(cube.GetOutput())

    # Actor.
    cubeActor = vtk.vtkActor()
    cubeActor.SetMapper(cubeMapper)
    cubeActor.GetProperty().SetColor(colors.GetColor3d("Banana"))

    # Assign actor to the renderer.
    ren.AddActor(cubeActor)

    ren.ResetCamera()
    ren.GetActiveCamera().Azimuth(30)
    ren.GetActiveCamera().Elevation(30)
    ren.ResetCameraClippingRange()
    ren.SetBackground(colors.GetColor3d("Silver"))

    # Enable user interface interactor.
    iren.Initialize()
    renWin.Render()
    WriteImage('TestCube', renWin, rgba=False)
    iren.Start()

def WriteImage(fileName, renWin, rgba=True):
    """
    Write the render window view to an image file.

    Image types supported are:
     BMP, JPEG, PNM, PNG, PostScript, TIFF.
    The default parameters are used for all writers, change as needed.

    :param fileName: The file name, if no extension then PNG is assumed.
    :param renWin: The render window.
    :param rgba: Used to set the buffer type.
    :return:
    """

    import os

    if fileName:
        # Select the writer to use.
        path, ext = os.path.splitext(fileName)
        ext = ext.lower()
        if not ext:
            ext = '.png'
            fileName = fileName + ext
        if ext == '.bmp':
            writer = vtk.vtkBMPWriter()
        elif ext == '.jpg':
            writer = vtk.vtkJPEGWriter()
        elif ext == '.pnm':
            writer = vtk.vtkPNMWriter()
        elif ext == '.ps':
            if rgba:
                rgba = False
            writer = vtk.vtkPostScriptWriter()
        elif ext == '.tiff':
            writer = vtk.vtkTIFFWriter()
        else:
            writer = vtk.vtkPNGWriter()

        windowto_image_filter = vtk.vtkWindowToImageFilter()
        windowto_image_filter.SetInput(renWin)
        windowto_image_filter.SetScale(1)  # image quality
        if rgba:
            windowto_image_filter.SetInputBufferTypeToRGBA()
        else:
            windowto_image_filter.SetInputBufferTypeToRGB()
            # Read from the front buffer.
            windowto_image_filter.ReadFrontBufferOff()
            windowto_image_filter.Update()

        writer.SetFileName(fileName)
        writer.SetInputConnection(windowto_image_filter.GetOutputPort())
        writer.Write()
    else:
        raise RuntimeError('Need a filename.')

if __name__ == "__main__":
    main()
