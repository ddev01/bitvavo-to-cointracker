import csv
from typing import Optional, Dict
import sys


class TransactionTransformer:
    """
    A class to transform transaction data from an input CSV file to an output CSV file.
    """

    def __init__(self, input_file: str, output_file: str) -> None:
        """
        Initializes the transformer with input and output file paths.

        :param input_file: Path to the input CSV file.
        :param output_file: Path to the output CSV file.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.fieldnames = [
            'Date',
            'Received Quantity',
            'Received Currency',
            'Sent Quantity',
            'Sent Currency',
            'Fee Amount',
            'Fee Currency',  # Corrected capitalization
            'Tag'
        ]

    def transform(self) -> None:
        """
        Transforms the input CSV data and writes the transformed data to the output CSV file.
        """
        try:
            with open(self.input_file, mode='r', newline='', encoding='utf-8') as csv_file, \
                 open(self.output_file, mode='w', newline='', encoding='utf-8') as csv_out_file:
                
                csv_reader = csv.DictReader(csv_file)
                csv_writer = csv.DictWriter(csv_out_file, fieldnames=self.fieldnames)
                csv_writer.writeheader()
                
                for row in csv_reader:
                    transformed_row = self._transform_row(row)
                    if transformed_row:
                        csv_writer.writerow(transformed_row)
        except FileNotFoundError as e:
            print(f"File not found: {e.filename}")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred during transformation: {e}")
            sys.exit(1)

    def _transform_row(self, row: Dict[str, str]) -> Optional[Dict[str, Optional[float]]]:
        """
        Transforms a single row of transaction data.

        :param row: A dictionary representing a row from the input CSV.
        :return: A dictionary representing the transformed row, or None if the row is invalid.
        """
        coin_date = f"{row['Date']} {row['Time'].split('.')[0]}"
        received_quantity: Optional[float] = None
        received_currency: Optional[str] = None
        sent_quantity: Optional[float] = None
        sent_currency: Optional[str] = None
        fee_amount: Optional[float] = None
        fee_currency: Optional[str] = None

        try:
            transaction_type = row['Type'].lower()
            if transaction_type == 'deposit':
                received_quantity = abs(float(row['Amount']))
                received_currency = row['Currency']
            elif transaction_type == 'withdrawal':
                sent_quantity = abs(float(row['Amount']))
                sent_currency = row['Currency']
                fee_amount = abs(float(row['Fee amount']))
                fee_currency = row['Fee currency']
            elif transaction_type == 'buy':
                received_quantity = abs(float(row['Amount']))
                received_currency = row['Currency']
                sent_quantity = abs(float(row['Received / Paid Amount']))
                sent_currency = 'EUR'
                fee_amount = abs(float(row['Fee amount']))
                fee_currency = row['Fee currency']
            elif transaction_type == 'sell':
                received_quantity = abs(float(row['Received / Paid Amount']))
                received_currency = 'EUR'
                sent_quantity = abs(float(row['Amount']))
                sent_currency = row['Currency']
                fee_amount = abs(float(row['Fee amount']))
                fee_currency = row['Fee currency']
            else:
                print(f"Unknown transaction type: {row['Type']}. Skipping row.")
                return None
        except KeyError as e:
            print(f"Missing expected column: {e}. Skipping row.")
            return None
        except ValueError as e:
            print(f"Value error: {e}. Skipping row.")
            return None

        return {
            'Date': coin_date,
            'Received Quantity': received_quantity,
            'Received Currency': received_currency,
            'Sent Quantity': sent_quantity,
            'Sent Currency': sent_currency,
            'Fee Amount': fee_amount,
            'Fee Currency': fee_currency,  # Corrected capitalization
            'Tag': ''
        }


def main() -> None:
    transformer = TransactionTransformer(
        input_file='history.csv',
        output_file='history_transformed.csv'
    )
    transformer.transform()
    print("Transformation complete.")


if __name__ == "__main__":
    main()