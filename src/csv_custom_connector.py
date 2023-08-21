import pathway as pw
import os
import glob


class CsvFileCustomConnector(pw.io.python.ConnectorSubject):

    def __init__(self, directory_path) -> None:
        super().__init__()
        self.directory_path = directory_path

    def process_file(self, file_path):
        with open(file_path) as file:
            column_names = None
            for index, line in enumerate(file):
                if index == 0:
                    column_names = line.strip().split(',')
                    continue
                values = line.strip().split(',')
                row_data = [f"{title}: {value}" for title, value in zip(column_names, values)]
                row_data = ', '.join(row_data)
                doc_object = {"doc": row_data}
                self.next_json(doc_object)

    def run(self):
        csv_files = glob.glob(os.path.join(self.directory_path, '*.csv'))

        for file_path in csv_files:
            self.process_file(file_path)
