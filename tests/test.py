import unittest
from unittest.mock import patch, Mock
from data_processing import process_data
from model_training import train_model
from scoring_service import start_service, score_data
from orchestration.task_definition import task_generate_data, task_process_data, task_train_model, task_start_service, task_score_data

class TestTasks(unittest.TestCase):

    @patch('data_generator.generate_data')
    def test_task_generate_data(self, mock_generate_data):
        # Arrange
        mock_generate_data.return_value = None
        ti = Mock()

        # Act
        task_generate_data(ti)

        # Assert
        mock_generate_data.assert_called_once()

    @patch('data_processing.process_data')
    def test_task_process_data(self, mock_process_data):
        # Arrange
        mock_process_data.return_value = None
        ti = Mock()

        # Act
        task_process_data(ti)

        # Assert
        mock_process_data.assert_called_once()

    @patch('model_training.train_model')
    def test_task_train_model(self, mock_train_model):
        # Arrange
        mock_train_model.return_value = None
        ti = Mock()

        # Act
        task_train_model(ti)

        # Assert
        mock_train_model.assert_called_once()

    @patch('scoring_service.start_service')
    def test_task_start_service(self, mock_start_service):
        # Arrange
        mock_start_service.return_value = None
        ti = Mock()

        # Act
        task_start_service(ti)

        # Assert
        mock_start_service.assert_called_once()

    @patch('scoring_service.score_data')
    def test_task_score_data(self, mock_score_data):
        # Arrange
        mock_score_data.return_value = None
        ti = Mock()

        # Act
        task_score_data(ti)

        # Assert
        mock_score_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()
