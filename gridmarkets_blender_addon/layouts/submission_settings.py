# ##### BEGIN GPL LICENSE BLOCK #####
#
# GridMarkets Blender Add-on - A Blender Add-on for rendering scenes / files on the Grid Computing network GridMarkets
# Copyright (C) 2019  GridMarkets
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

from gridmarkets_blender_addon import constants, utils_blender


def draw_submission_summary(self, context):
    scene = context.scene
    props = scene.props
    open = props.submission_summary_open

    box = self.layout.box()

    col = box.column()
    row = col.row(align=True)
    row.alignment = 'LEFT'

    row.operator(
        constants.OPERATOR_TOGGLE_SUBMISSION_SUMMARY_ID_NAME,
        text="Submission Summary",
        icon=constants.ICON_DISCLOSURE_TRI_DOWN if open else constants.ICON_DISCLOSURE_TRI_RIGHT,
        emboss=False,
    )

    if open:
        split = col.split(percentage=0.2)
        labels = split.column()
        labels.label(text="Project: ")
        labels.separator()
        labels.label(text="Job: ")
        labels.label(text="App: ")
        labels.label(text="App Version: ")
        labels.label(text="GM Operation: ")
        labels.label(text="Path: ")
        labels.label(text="Frame range(s): ")
        labels.label(text="Output prefix: ")
        labels.label(text="Output format: ")
        labels.label(text="Output path: ")
        labels.label(text="Render Engine: ")
        labels.label(text="Resolution X: ")
        labels.label(text="Resolution Y: ")
        labels.label(text="Resolution %: ")
        labels.label(text="Frame Rate: ")

        values = split.column()
        if props.project_options == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            values.label(text=constants.PROJECT_OPTIONS_NEW_PROJECT_DESCRIPTION)
        else:
            project = props.projects[int(props.project_options) - constants.PROJECT_OPTIONS_STATIC_COUNT]
            values.label(text=project.name)
        values.separator()

        if props.job_options == constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE:
            values.label(text=constants.JOB_OPTIONS_BLENDERS_SETTINGS_LABEL)
        else:
            selected_job = props.jobs[int(props.job_options) - constants.JOB_OPTIONS_STATIC_COUNT]
            values.label(text=selected_job.name)

        # get a gridmarkets job. The render file doesnt matter for now
        job = utils_blender.get_job(context, "RENDER FILE")
        values.label(text=job.app)
        values.label(text=job.app_version)
        values.label(text=job.operation)
        values.label(text=job.path)
        values.label(text=job.params['frames'])
        values.label(text='' if job.params['output_prefix'] is None else job.params['output_prefix'])
        values.label(text=job.params['output_format'])
        values.label(text=utils_blender.get_job_output_path_abs(context))
        values.label(text=job.params['engine'])
        values.label(text=str(scene.render.resolution_x))
        values.label(text=str(scene.render.resolution_y))
        values.label(text=str(scene.render.resolution_percentage) + ' %')
        values.label(text=str(scene.render.fps))


def draw_submission_settings(self, context):
    layout = self.layout

    props = context.scene.props

    # submit box
    box = layout.box()
    row = box.row()

    # project options
    col = row.column(align=True)
    col.label(text="Project")
    sub = col.row()
    sub.enabled = False
    sub.label(text="The project to run the selected job against.")
    col.separator()
    col.prop(props, "project_options", text="")

    # job options
    col = row.column(align=True)
    col.label(text="Job")
    sub = col.row()
    sub.enabled = False
    sub.label(text="The render settings and output settings to use.")
    col.separator()
    col.prop(props, "job_options", text="")

    submit_text = "Submit"
    submit_icon = "NONE"

    # submit button / progress indicator
    row = box.row(align=True)
    row.scale_y = 2.5
    if props.submitting_project:
        row.prop(props, "submitting_project_progress", text=props.submitting_project_status)
    else:
        # disable submit button when uploading project
        if props.uploading_project:
            row.enabled = False

        # if the engine is not in the supported engines list disable and show a help message
        render_engine = utils_blender.get_job_render_engine(context)
        if render_engine not in utils_blender.get_supported_render_engines():
            row.enabled = False
            submit_text = "Render engine '%s' is not currently supported" % utils_blender.get_user_friendly_name_for_engine(
                render_engine)
            submit_icon = constants.ICON_ERROR

        row.operator(constants.OPERATOR_SUBMIT_ID_NAME, text=submit_text, icon=submit_icon)