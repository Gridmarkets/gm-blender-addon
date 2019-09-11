from gridmarkets_blender_addon.meta_plugin.scene_exporter import SceneExporter

import bpy
import pathlib

from gridmarkets_blender_addon.project.packed_vray_project import PackedVRayProject

_un_modified_render_method = None


def export_vray_scene(engine, scene):

    if _un_modified_render_method is None:
        raise ValueError("Unmodified render method un-set")

    _un_modified_render_method(engine, scene)


class VRaySceneExporter(SceneExporter):

    def export(self, output_dir: pathlib.Path) -> PackedVRayProject:
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        log = PluginFetcher.get_plugin().get_logging_coordinator().get_logger(__name__)

        try:
            import vb30
        except ImportError:
            log.error("Unable to import V-Ray addon (vb30)")
            raise ImportError

        # export the scene to the output directory
        scene = bpy.context.scene
        VRayExporter = scene.vray.Exporter

        # remember user settings
        autorun = VRayExporter.autorun
        useSeparateFiles = VRayExporter.useSeparateFiles
        app_output_dir = VRayExporter.output_dir

        # store the un modified render method (overridden later)
        global _un_modified_render_method
        _un_modified_render_method = vb30.export.RenderScene

        try:
            # change the exporter settings for our purposes
            VRayExporter.autorun = False            # don't render the scene
            VRayExporter.useSeparateFiles = True    # export as separate files in case of differential file uploading
            VRayExporter.output_dir = str(output_dir)

            # override the default VRay render eninge render method
            vb30.export.RenderScene = export_vray_scene

            # now calling the render operator will export the scene for us
            bpy.ops.render.render()

        finally:
            # reset all settings to what they were before exporting
            VRayExporter.autorun = autorun
            VRayExporter.useSeparateFiles = useSeparateFiles
            VRayExporter.output_dir = app_output_dir
            vb30.export.RenderScene = _un_modified_render_method

        return PackedVRayProject(output_dir, output_dir / "scene_scene.vrscene")
