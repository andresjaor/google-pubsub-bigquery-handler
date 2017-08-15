# -*- coding: utf-8 -*-
import logging
from google.cloud import bigquery
from google.appengine.api import background_thread


class BqClient:
    def __init__(self):
        self.client = bigquery.Client()

    def insert_row(self, data_set, table, data):
        background_thread.start_new_background_thread(self._insert_row, [data_set, table, data])

    def _insert_row(self, data_set, table, data):
        try:
            dataset = self.client.dataset(data_set)
            _table = dataset.table(table)
            _table.reload()
            if not isinstance(data, list):
                reg = []
                for column in _table.schema:
                    reg.append(data.get(column.name.lower(), None))
                error = _table.insert_data([tuple(reg)], ignore_unknown_values=True)
                logging.info("Message inserted to schema: %s:%s -> data:%s -> errors:%s" %
                             (data_set, table, [tuple(reg)], error))
            else:
                rows = []
                for x in data:
                    reg = []
                    for column in _table.schema:
                        reg.append(x.get(column.name.lower(), None))
                    rows.append(tuple(reg))
                error = _table.insert_data(rows, ignore_unknown_values=True)
                logging.info("Message inserted to schema: %s:%s -> data:%s mensajes -> errors:%s" %
                             (data_set, table, len(rows), error))
        except Exception as e:
            logging.error("Error streaming data to BigQuery: %s" % e)
            pass
