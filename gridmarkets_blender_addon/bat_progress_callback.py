from blender_asset_tracer.pack.progress import Callback
import pathlib
import typing


class BatProgressCallback(Callback):
    """ Represents a callback class which logs the progress made by BAT.pack and BAT.trace"""

    def __init__(self, logger):
        """ Constructor
        :param logger: The logger instance which should be used to log the progress
        :type logger: blender_logging_wrapper.BlenderLoggingWrapper
        """
        self.log = logger

    def pack_start(self) -> None:
        self.log.info('Starting BAT Pack operation')

    def pack_done(self,
                  output_blendfile: pathlib.Path,
                  missing_files: typing.Set[pathlib.Path]) -> None:
        if missing_files:
            self.log.info('There were %d missing files' % len(missing_files))
        else:
            self.log.info('Pack of %s done' % output_blendfile.name)

    def pack_aborted(self, reason: str):
        self.log.info('Aborted: %s' % reason)

    def trace_blendfile(self, filename: pathlib.Path) -> None:
        """Called for every .blend file opened when tracing dependencies."""
        self.log.info('Inspecting %s' % filename.name)

    def trace_asset(self, filename: pathlib.Path) -> None:
        if filename.stem == '.blend':
            return
        self.log.info('Found asset %s' % filename.name)

    def rewrite_blendfile(self, orig_filename: pathlib.Path) -> None:
        self.log.info('Rewriting cloned %s (This will not modify your original file / scene)' % orig_filename.name)

    def transfer_file(self, src: pathlib.Path, dst: pathlib.Path) -> None:
        self.log.info('Transferring %s' % src.name)

    def transfer_file_skipped(self, src: pathlib.Path, dst: pathlib.Path) -> None:
        self.log.info('Skipped %s' % src.name)

    def transfer_progress(self, total_bytes: int, transferred_bytes: int) -> None:
        self.log.info("Progress: %s" % str(round(100 * transferred_bytes / total_bytes)))

    def missing_file(self, filename: pathlib.Path) -> None:
        self.log.warning("Missing asset: %s" % filename.name)
        pass
