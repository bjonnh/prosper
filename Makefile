all:	prosper_ui.py prosper_dialog_wait_ui.py prosper_dialog_racks_ui.py prosper_dialog_logger_ui.py prosper_dialog_config_ui.py prosper_dialog_add_action_ui.py prosper_rc.py

prosper_ui.py: prosper.ui
	pyuic4 prosper.ui > prosper_ui.py
prosper_dialog_wait_ui.py: prosper_dialog_wait.ui
	pyuic4 prosper_dialog_wait.ui > prosper_dialog_wait_ui.py
prosper_dialog_racks_ui.py: prosper_dialog_racks.ui
	pyuic4 prosper_dialog_racks.ui > prosper_dialog_racks_ui.py
prosper_dialog_logger_ui.py: prosper_dialog_logger.ui
	pyuic4 prosper_dialog_logger.ui > prosper_dialog_logger_ui.py
prosper_dialog_config_ui.py: prosper_dialog_config.ui
	pyuic4 prosper_dialog_config.ui > prosper_dialog_config_ui.py
prosper_dialog_add_action_ui.py: prosper_dialog_add_action.ui
	pyuic4 prosper_dialog_add_action.ui > prosper_dialog_add_action_ui.py
prosper_rc.py: prosper.qrc
	pyrcc4 -py3 prosper.qrc > prosper_rc.py

svgs: 
	rm -f images/*.svg
	./opt_svgs.sh &> /dev/null

clean:
#	rm -f images/*.svg
	rm -f prosper_ui.py
	rm -f prosper_dialog_racks_ui.py
	rm -f prosper_dialog_config_ui.py
	rm -f prosper_rc.py
