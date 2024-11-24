# # from wetranslateai.app.worker.worker import celery

# # @celery.task
# # def task_test():
# #     result = "hello"
# #     return f"Task B completed! Called: {result}"
# @patch("worker.create_task.run")
# def test_mock_task(mock_run):
#     assert create_task.run(1)
#     create_task.run.assert_called_once_with(1)

#     assert create_task.run(2)
#     assert create_task.run.call_count == 2

#     assert create_task.run(3)
#     assert create_task.run.call_count == 3
