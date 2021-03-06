DELETE FROM topic_wf; 

DELETE FROM wf_nextflow;

DELETE FROM contributor; 

DELETE FROM person_git_comp; 

DELETE FROM similarity_process; 

DELETE FROM link_process_channel; 

DELETE FROM link_channel_operation; 

DELETE FROM tools_have_topic; 

DELETE FROM topic_tools; 

DELETE FROM tool_in_workflow; 

DELETE FROM tool_in_process; 

DELETE FROM tools_have_in_out; 

DELETE FROM in_out_data; 

DELETE FROM tools_have_operation; 

DELETE FROM operation_tool; 

DELETE FROM tool; 

DELETE FROM channel;

DELETE FROM operation_wf; 

DELETE FROM process; 

DELETE FROM workflow; 

DELETE FROM person_git; 

----------------------------------------------------

ALTER SEQUENCE seq_id_process RESTART WITH 1; 

ALTER SEQUENCE seq_id_wf RESTART WITH 1; 

ALTER SEQUENCE seq_id_channel RESTART WITH 1; 

ALTER SEQUENCE seq_id_operation_wf RESTART WITH 1; 

ALTER SEQUENCE seq_id_in_out_tool RESTART WITH 1; 

ALTER SEQUENCE seq_id_topic_tools RESTART WITH 1; 

ALTER SEQUENCE seq_id_operation_tools RESTART WITH 1; 