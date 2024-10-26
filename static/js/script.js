const apiUrl = 'http://localhost:5000/api';

document.addEventListener("DOMContentLoaded", () => {
    loadTableOptions(); // Завантажуємо доступні таблиці
    document.getElementById('tableSelect').addEventListener('change', loadTableData);
});

// Завантаження списку таблиць для вибору
async function loadTableOptions() {
    try {
        const response = await fetch(`${apiUrl}/get-tables`);
        const tables = await response.json();
        const tableSelect = document.getElementById('tableSelect');
        tableSelect.innerHTML = '<option value="">Оберіть таблицю</option>'; // Очищаємо попередні опції
        tables.forEach(table => {
            const option = document.createElement('option');
            option.value = table;
            option.textContent = table;
            tableSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Помилка завантаження таблиць:', error);
    }
}

// Завантаження заголовків таблиці та рядків для обраної таблиці
async function loadTableData() {
    const tableName = document.getElementById('tableSelect').value;
    if (!tableName) return; // Якщо таблиця не обрана, виходимо з функції

    try {
        // Отримуємо заголовки (колонки)
        const columnResponse = await fetch(`${apiUrl}/get-columns/${tableName}`);
        const columns = await columnResponse.json();

        const columnSelect = document.getElementById('columnSelect');
        const tableHeaders = document.getElementById('tableHeaders');
        const tableRows = document.getElementById('tableRows');
        tableHeaders.innerHTML = ''; // Очищаємо попередні заголовки
        tableRows.innerHTML = ''; // Очищаємо попередні заголовки
        columnSelect.innerHTML = ''; // Очищаємо попередні опції колонок

        columns.forEach(column => {
            const option = document.createElement("option");
            option.value = column.name;
            option.textContent = column.name + `(${column.type})`;
            columnSelect.appendChild(option); // Додаємо опцію для колонок

            const th = document.createElement('th');
            th.textContent = column.name + `(${column.type})`; // Додаємо заголовок таблиці
            tableHeaders.appendChild(th);
        });

        // Додаємо рядок для вводу нових даних
        const inputRow = document.createElement('tr');

        columns.forEach(column => {
            const td = document.createElement('td');
            if (column.name !== 'id') {
                let input;

                // Визначаємо тип інпуту в залежності від типу даних колонки
                if (column.type === 'boolean') {
                    input = document.createElement('input');
                    input.type = 'checkbox'; // Чекбокс для булевих значень
                } else if (column.type === 'date') {
                    input = document.createElement('input');
                    input.type = 'date'; // Інпут для вибору дати
                } else if (column.type === 'int' || column.type === 'bigint' || column.type === 'smallint' || column.type === 'tinyint') {
                    input = document.createElement('input');
                    input.type = 'number'; // Інпут для цілочисельних значень
                    input.step = '1'; // Приймаємо лише цілочисельні значення
                    input.min = Number.MIN_SAFE_INTEGER; // Мінімально допустиме значення
                    input.max = Number.MAX_SAFE_INTEGER; // Максимально допустиме значення
                } else if (column.type === 'float' || column.type === 'double') {
                    input = document.createElement('input');
                    input.type = 'number'; // Інпут для чисел з плаваючою крапкою
                    input.step = '0.01'; // Приймаємо дробові значення
                } else if (column.type.startsWith('decimal')) {
                    input = document.createElement('input');
                    input.type = 'number'; // Інпут для десяткових чисел
                    input.step = '0.01'; // Приймаємо дробові значення
                } else {
                    input = document.createElement('input');
                    input.type = 'text'; // Текстове поле для інших типів
                }

                td.appendChild(input); // Додаємо інпут до клітинки
            }
            inputRow.appendChild(td); // Додаємо клітинку до рядка вводу
        });

        // Додаємо кнопку "додати" для рядка вводу
        const addButtonCell = document.createElement('td');
        const addButton = document.createElement('button');
        addButton.textContent = 'Додати';
        addButton.classList.add('btn', 'btn-primary'); // Додаємо Bootstrap класи
        addButton.onclick = () => addRow(inputRow); // Виклик функції для додавання рядка
        addButtonCell.appendChild(addButton);
        inputRow.appendChild(addButtonCell); // Додаємо кнопку до рядка вводу

        // Додаємо рядок для вводу даних на початок таблиці
        tableRows.prepend(inputRow); // Додаємо новий рядок на початок

        // Отримуємо рядки (дані)
        const rowResponse = await fetch(`${apiUrl}/get-rows/${tableName}`);
        const rows = await rowResponse.json();
        rows.forEach(row => {
            const tr = document.createElement('tr');
            const values = Object.values(row);
            for (let i = 0; i < values.length; i++) {
                const td = document.createElement('td');
                td.textContent = values[i]; // Додаємо дані в клітинки
                td.setAttribute("data-columnName", columns[i].name);
                td.setAttribute("data-columnType", columns[i].type);
                tr.appendChild(td);
            }

            // Додаємо кнопки "редагувати" і "видалити"
            const editButtonCell = document.createElement('td');
            const editButton = document.createElement('button');
            editButton.textContent = 'Редагувати';
            editButton.classList.add('btn', 'btn-warning'); // Додаємо Bootstrap класи
            editButton.onclick = () => editRow(row); // Виклик функції для редагування рядка
            editButtonCell.appendChild(editButton);

            const deleteButtonCell = document.createElement('td');
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Видалити';
            deleteButton.classList.add('btn', 'btn-danger'); // Додаємо Bootstrap класи
            deleteButton.onclick = () => deleteRow(row[0]); // Виклик функції для видалення рядка
            deleteButtonCell.appendChild(deleteButton);

            tr.appendChild(editButtonCell); // Додаємо кнопку редагування
            tr.appendChild(deleteButtonCell); // Додаємо кнопку видалення
            tableRows.appendChild(tr); // Додаємо рядок до таблиці  }

        });
    } catch (error) {
        console.error('Помилка завантаження даних таблиці:', error);
    }
}


// Функція для додавання нового рядка
async function addRow(inputRow) {
    const tableName = document.getElementById('tableSelect').value;
    if (!tableName) return; // Якщо таблиця не обрана, виходимо з функції
    const newData = {};
    const inputs = inputRow.getElementsByTagName('input');

    // Збираємо дані з інпутів
    for (let i = 0; i < inputs.length; i++) {
        const columnName = document.getElementById('columnSelect').options[i + 1].value;

        // Determine the input type and handle accordingly
        if (inputs[i].type === 'checkbox') {
            newData[columnName] = inputs[i].checked;
        } else if (inputs[i].type === 'number') {
            // Convert to a number if it's a numeric input
            newData[columnName] = inputs[i].value ? Number(inputs[i].value) : null;
        } else {
            newData[columnName] = inputs[i].value;
        }
    }

    try {
        // Відправляємо запит на сервер для додавання рядка
        const response = await fetch(`${apiUrl}/add-row/${tableName}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newData),
        });

        if (response.ok) {
            console.log('Рядок додано успішно');
            // Оновлюємо таблицю для відображення нових даних
            await loadTableData();
        } else {
            console.error('Помилка при додаванні рядка:', response.statusText);
        }
    } catch (error) {
        console.error('Помилка при додаванні рядка:', error);
    }
}

// Функція для редагування рядка
function editRow(row) {
    console.log('Редагування рядка:', row);
    // Реалізуйте логіку редагування тут
}

// Функція для видалення рядка
async function deleteRow(rowId) {
    const tableName = document.getElementById('tableSelect').value;
    if (!tableName) return; // Якщо таблиця не обрана, виходимо з функції
    try {
        const response = await fetch(`${apiUrl}/delete-row/${tableName}/${rowId}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            console.log('Рядок видалено успішно');
            // Оновлюємо таблицю для відображення нових даних
            loadTableData();
        } else {
            console.error('Помилка при видаленні рядка:', response.statusText);
        }
    } catch (error) {
        console.error('Помилка при видаленні рядка:', error);
    }
}



// Створення нової таблиці
async function createTable() {
    const tableName = document.getElementById('createTableName').value;
    if (!tableName) {
        alert("Будь ласка, введіть назву таблиці."); // Попередження, якщо не введено назву
        return;
    }

    try {
        const response = await fetch(`${apiUrl}/add-table`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                table_name: tableName
            })
        });
        const data = await response.json();
        console.log('Таблицю створено:', data);
        loadTables(); // Оновлюємо список таблиць після створення
        document.getElementById('createTableName').value = ''; // Очищаємо поле введення
    } catch (error) {
        console.error('Помилка створення таблиці:', error);
    }
}

// Видалення обраної таблиці
async function deleteTable() {
    const tableName = document.getElementById('tableSelect').value;
    if (!tableName) {
        alert("Будь ласка, виберіть таблицю для видалення."); // Попередження, якщо таблиця не обрана
        return;
    }

    if (confirm(`Ви впевнені, що хочете видалити таблицю "${tableName}"?`)) {
        try {
            const response = await fetch(`${apiUrl}/delete-table`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    table_name: tableName
                })
            });
            const data = await response.json();
            console.log('Таблицю видалено:', data);
            loadTables(); // Оновлюємо список таблиць після видалення
        } catch (error) {
            console.error('Помилка видалення таблиці:', error);
        }
    }
}

// Додавання нової колонки
async function addColumn() {
    const tableName = document.getElementById('tableSelect').value;
    const columnName = document.getElementById('addColumnName').value;
    const columnType = document.getElementById('addColumnType').value;

    if (!tableName || !columnName) {
        alert("Будь ласка, виберіть таблицю та введіть назву колонки."); // Попередження, якщо не вибрано таблицю чи не введено назву
        return;
    }

    try {
        const response = await fetch(`${apiUrl}/add-column`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                table_name: tableName,
                column_name: columnName,
                column_type: columnType
            })
        });
        const data = await response.json();
        console.log('Колонку додано:', data);
        loadTableData(); // Оновлюємо дані таблиці після додавання колонки
        document.getElementById('addColumnName').value = ''; // Очищаємо поле введення
    } catch (error) {
        console.error('Помилка додавання колонки:', error);
    }
}

// Перейменування обраної колонки
async function renameColumn() {
    const tableName = document.getElementById('tableSelect').value;
    const oldColumnName = document.getElementById('columnSelect').value;
    const newColumnName = document.getElementById('newColumnName').value;

    if (!tableName || !oldColumnName || !newColumnName) {
        alert("Будь ласка, виберіть колонку та введіть нову назву."); // Попередження, якщо не вибрано колонку або не введено нову назву
        return;
    }

    try {
        const response = await fetch(`${apiUrl}/rename-column`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                table_name: tableName,
                old_name: oldColumnName,
                new_name: newColumnName
            })
        });
        const data = await response.json();
        console.log('Колонку перейменовано:', data);
        loadTableData(); // Оновлюємо дані таблиці після перейменування
        document.getElementById('newColumnName').value = ''; // Очищаємо поле введення
    } catch (error) {
        console.error('Помилка перейменування колонки:', error);
    }
}

// Видалення обраної колонки
async function deleteColumn() {
    const tableName = document.getElementById('tableSelect').value;
    const columnName = document.getElementById('columnSelect').value;

    if (!tableName || !columnName) {
        alert("Будь ласка, виберіть колонку для видалення."); // Попередження, якщо не вибрано колонку
        return;
    }

    try {
        const response = await fetch(`${apiUrl}/delete-column`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                table_name: tableName,
                column_name: columnName
            })
        });
        const data = await response.json();
        console.log('Колонку видалено:', data);
        loadTableData(); // Оновлюємо дані таблиці після видалення колонки
    } catch (error) {
        console.error('Помилка видалення колонки:', error);
    }
}

// Завантаження таблиць у випадаючий список tableSelect
async function loadTables() {
    try {
        const response = await fetch(`${apiUrl}/get-tables`);
        const tables = await response.json();
        const tableSelect = document.getElementById('tableSelect');
        tableSelect.innerHTML = '<option value="">Оберіть таблицю</option>'; // Очищаємо існуючі опції
        tables.forEach(table => {
            const option = document.createElement('option');
            option.value = table;
            option.textContent = table;
            tableSelect.appendChild(option); // Додаємо опцію таблиці
        });
    } catch (error) {
        console.error('Помилка завантаження таблиць:', error);
    }
}