// Define the path to the CSV file
const csvFilePathEmails = 'data//data_emails.csv';
console.log(csvFilePathEmails)

// Define the column headers for the HTML table
const tableHeadersEmails = ['Subject', 'Sender Name', 'Sender Address', 'Date'];

// Define a function to convert CSV data to an array of objects
function csvToArray(csvData) {
  const lines = csvData.split('\n');
  const result = [];
  const headers = lines[0].split(',');

  for (let i = 1; i < lines.length; i++) {
    const obj = {};
    const currentline = lines[i].split(',');

    for (let j = 0; j < headers.length; j++) {
      obj[headers[j]] = currentline[j];
    }

    result.push(obj);
  }

  return result;
}

// Use jQuery to read the CSV file and populate the HTML table
$(document).ready(function() {
  $.ajax({
    type: 'GET',
    url: csvFilePathEmails,
    success: function(data) {
      const csvArray = csvToArray(data);

      const table = $('<table>').addClass('table');
      const thead = $('<thead>');
      const tbody = $('<tbody>');

      // Add the table headers to the table
      const headerRow = $('<tr>');
      tableHeadersEmails.forEach(function(header) {
        headerRow.append($('<th>').text(header));
      });
      thead.append(headerRow);
      table.append(thead);

      // Add the data rows to the table
      csvArray.forEach(function(rowData) {
        const row = $('<tr>');
        Object.values(rowData).forEach(function(val) {
          row.append($('<td>').text(val));
        });
        tbody.append(row);
      });
      table.append(tbody);

      // Add some basic styling to the table
      table.addClass('table');
      table.addClass('table-striped');
      table.addClass('table-bordered');

      // Add the table to the HTML page
      $('#emails-container').append(table);
    }
  });
});
