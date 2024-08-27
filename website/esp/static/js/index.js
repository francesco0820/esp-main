document.addEventListener("DOMContentLoaded", function() {
    applyFilters();
});

function toggleFilters() {
    console.log("Toggle button clicked");
    const filtersSection = document.getElementById('filters-section');
    const toggleButton = document.querySelector('.toggle-filters');
    if (filtersSection.style.display === 'none' || filtersSection.style.display === '') {
        filtersSection.style.display = 'block';
        toggleButton.textContent = 'Hide Filters';
    } else {
        filtersSection.style.display = 'none';
        toggleButton.textContent = 'Show Filters';
    }
}

function resetFilters() {
    const operators = ['industry', 'position', 'company', 'theme'];
    operators.forEach(field => {
        document.getElementById(`${field}-operator`).value = 'all';
        document.getElementById(`${field}-options`).innerHTML = '<option value="all"></option>';
        document.getElementById(`${field}-options`).disabled = false;
    });

    document.getElementById('executive-name').value = '';
    document.getElementById('executive-suggestions').innerHTML = '';

    document.getElementById('date-start').value = '';
    document.getElementById('date-end').value = '';

    const filtersSection = document.getElementById('filters-section');
    if (filtersSection.style.display === 'block') {
        filtersSection.style.display = 'none';
        document.querySelector('.toggle-filters').textContent = 'Show Filters';
    }

    applyFilters();
}

function populateOptions(field) {
    const operator = document.getElementById(`${field}-operator`).value;
    const optionsSelect = document.getElementById(`${field}-options`);

    optionsSelect.innerHTML = '<option value="all"></option>';
    optionsSelect.multiple = false; // Reset to single selection by default
    optionsSelect.disabled = false;

    switch (operator) {
        case 'has_any':
        case 'has_all':
        case 'has_none':
            optionsSelect.multiple = true; // Allow multiple selections
            fetchOptionsFromDatabase(field, operator, optionsSelect);
            break;
        case 'is_exactly':
            optionsSelect.multiple = false; // Single selection only
            fetchOptionsFromDatabase(field, operator, optionsSelect);
            break;
        case 'is_empty':
        case 'is_not_empty':
            optionsSelect.disabled = true; // Disable the dropdown
            break;
        default:
            fetchOptionsFromDatabase(field, operator, optionsSelect);
            break;
    }
}

function fetchOptionsFromDatabase(field, operator, optionsSelect) {
    fetch(`/get-options/${field}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ operator: operator }),
    })
    .then(response => response.json())
    .then(data => {
        optionsSelect.innerHTML = '';  // Clear any existing options
        data.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            optionsSelect.appendChild(optionElement);
        });
    });
}

function fetchExecutiveSuggestions(query) {
    if (query.length < 2) { // Start suggesting after 2 characters
        document.getElementById('executive-suggestions').innerHTML = '';
        return;
    }

    fetch(`/get-executives/?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const suggestionsDiv = document.getElementById('executive-suggestions');
            suggestionsDiv.innerHTML = '';  // Clear any existing suggestions

            data.forEach(executive => {
                const suggestionItem = document.createElement('div');
                suggestionItem.textContent = executive;
                suggestionItem.onclick = () => selectExecutive(executive);
                suggestionsDiv.appendChild(suggestionItem);
            });
        });
}

function selectExecutive(executiveName) {
    document.getElementById('executive-name').value = executiveName;
    document.getElementById('executive-suggestions').innerHTML = '';  // Clear suggestions once selected
}

function applyFilters() {
    const filters = {
        industry: {
            operator: document.getElementById('industry-operator').value,
            value: Array.from(document.getElementById('industry-options').selectedOptions).map(option => option.value)
        },
        position: {
            operator: document.getElementById('position-operator').value,
            value: Array.from(document.getElementById('position-options').selectedOptions).map(option => option.value)
        },
        company: {
            operator: document.getElementById('company-operator').value,
            value: Array.from(document.getElementById('company-options').selectedOptions).map(option => option.value)
        },
        theme: {
            operator: document.getElementById('theme-operator').value,
            value: Array.from(document.getElementById('theme-options').selectedOptions).map(option => option.value)
        },
        date: {
            start: document.getElementById('date-start').value,
            end: document.getElementById('date-end').value
        },
        executive: {
            name: document.getElementById('executive-name').value
        }
    };

    // Only include filters that are not 'all', have a value, or have a valid date range
    for (let key in filters) {
        if (
            (filters[key].operator === 'all') || 
            (filters[key].value && filters[key].value.length === 0) ||
            (key === 'date' && !filters.date.start && !filters.date.end)
        ) {
            delete filters[key];
        }
    }

    fetch('/filter/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: filters })
    })
    .then(response => response.json())
    .then(data => {
        // Update the summary data
        document.getElementById('unique-audience').textContent = data.unique_audience_members;
        document.getElementById('unique-posts').textContent = data.total_unique_posts;
        document.getElementById('total-engagements').textContent = data.total_engagements;
        document.getElementById('average-engagements').textContent = data.average_engagements_per_post;

        // Fetch and update the Posts vs Engagements Chart
        fetchPostsEngagementsData();
        fetchTopExecutivesData();
        fetchPostsVolumeData();
        fetchEngagementsVolumeData();
        fetchTopThemesByPostVolData();
        fetchTopThemesByEngagementVolData();
        fetchContentFormatsPostsChartData();
        fetchContentFormatsEngagementsChartData();
        fetchTopPostsData();
    });
}

function getFilters() {
    return {
        industry: {
            operator: document.getElementById('industry-operator').value,
            value: Array.from(document.getElementById('industry-options').selectedOptions).map(option => option.value)
        },
        position: {
            operator: document.getElementById('position-operator').value,
            value: Array.from(document.getElementById('position-options').selectedOptions).map(option => option.value)
        },
        company: {
            operator: document.getElementById('company-operator').value,
            value: Array.from(document.getElementById('company-options').selectedOptions).map(option => option.value)
        },
        theme: {
            operator: document.getElementById('theme-operator').value,
            value: Array.from(document.getElementById('theme-options').selectedOptions).map(option => option.value)
        },
        date: {
            start: document.getElementById('date-start').value,
            end: document.getElementById('date-end').value
        },
        executive: {
            name: document.getElementById('executive-name').value
        }
    };
}

let postsEngagementsChart;

function fetchPostsEngagementsData() {
    const filters = getFilters();
    fetch('/chart-data/posts-engagements', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: filters })
    })
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('postsEngagementsChart').getContext('2d');

        // Check if the chart already exists and destroy it before creating a new one
        if (postsEngagementsChart) {
            postsEngagementsChart.destroy();
        }

        postsEngagementsChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Posts', 'Engagements'],
                datasets: [{
                    label: 'Count',
                    data: [data.post_count, data.engagement_count],
                    backgroundColor: ['rgba(54, 162, 235, 0.6)', 'rgba(255, 99, 132, 0.6)'],
                    borderColor: ['rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)'],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
}

let postsVolumeChart;

function fetchPostsVolumeData() {
    const filters = getFilters();

    fetch('/chart-data/posts-volume', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: filters })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Original Chart Data:', data);

        // Mapping month names to numbers
        const monthMap = {
            'January': '01',
            'February': '02',
            'March': '03',
            'April': '04',
            'May': '05',
            'June': '06',
            'July': '07',
            'August': '08',
            'September': '09',
            'October': '10',
            'November': '11',
            'December': '12'
        };

        // Convert the dates to 'yyyy-MM-dd' format
        const formattedDates = data.dates.map(dateStr => {
            const [year, monthName, day] = dateStr.split('-');
            const month = monthMap[monthName];
            const formattedDay = day.padStart(2, '0');  // Ensure day is two digits
            return `${year}-${month}-${formattedDay}`;
        });

        console.log('Formatted Dates:', formattedDates);

        // Prepare data for scatter plot
        const scatterData = formattedDates.map((date, index) => ({
            x: new Date(date),
            y: data.post_counts[index]
        }));

        // Calculate the trendline using linear regression
        const xValues = scatterData.map(point => point.x.getTime());
        const yValues = scatterData.map(point => point.y);
        const regression = ss.linearRegression(scatterData.map(point => [point.x.getTime(), point.y]));
        const trendlinePoints = scatterData.map(point => ({
            x: point.x,
            y: ss.linearRegressionLine(regression)(point.x.getTime())
        }));

        const ctx = document.getElementById('postsVolumeChart').getContext('2d');

        // Check if the chart already exists and destroy it before creating a new one
        if (postsVolumeChart) {
            postsVolumeChart.destroy();
        }

        postsVolumeChart = new Chart(ctx, {
            type: 'scatter',  // Specify the chart type as 'scatter'
            data: {
                datasets: [{
                    label: 'Post Volume',
                    data: scatterData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                }, {
                    label: 'Trendline',
                    data: trendlinePoints,
                    type: 'line',  // Plot the trendline as a line chart
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    fill: false,
                    pointRadius: 0  // Hide the points on the trendline
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            tooltipFormat: 'yyyy-MM-dd',
                            displayFormats: {
                                day: 'yyyy-MM-dd'
                            }
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Post Volume'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return `(${tooltipItem.raw.x.toISOString().split('T')[0]}, ${tooltipItem.raw.y})`;
                            }
                        }
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching chart data:', error);
    });
}

let engagementsVolumeChart;

function fetchEngagementsVolumeData() {
    const filters = getFilters();

    fetch('/chart-data/engagements-volume', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: filters })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Original Chart Data:', data);

        // Mapping month names to numbers
        const monthMap = {
            'January': '01',
            'February': '02',
            'March': '03',
            'April': '04',
            'May': '05',
            'June': '06',
            'July': '07',
            'August': '08',
            'September': '09',
            'October': '10',
            'November': '11',
            'December': '12'
        };

        // Convert the dates to 'yyyy-MM-dd' format
        const formattedDates = data.dates.map(dateStr => {
            const [year, monthName, day] = dateStr.split('-');
            const month = monthMap[monthName];
            const formattedDay = day.padStart(2, '0');  // Ensure day is two digits
            return `${year}-${month}-${formattedDay}`;
        });

        console.log('Formatted Dates:', formattedDates);

        // Prepare data for scatter plot
        const scatterData = formattedDates.map((date, index) => ({
            x: new Date(date),
            y: data.engagement_counts[index]
        }));

        // Calculate the trendline using linear regression
        const xValues = scatterData.map(point => point.x.getTime());
        const yValues = scatterData.map(point => point.y);
        const regression = ss.linearRegression(scatterData.map(point => [point.x.getTime(), point.y]));
        const trendlinePoints = scatterData.map(point => ({
            x: point.x,
            y: ss.linearRegressionLine(regression)(point.x.getTime())
        }));

        const ctx = document.getElementById('engagementsVolumeChart').getContext('2d');

        // Check if the chart already exists and destroy it before creating a new one
        if (engagementsVolumeChart) {
            engagementsVolumeChart.destroy();
        }

        engagementsVolumeChart = new Chart(ctx, {
            type: 'scatter',  // Specify the chart type as 'scatter'
            data: {
                datasets: [{
                    label: 'Engagement Volume',
                    data: scatterData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                }, {
                    label: 'Trendline',
                    data: trendlinePoints,
                    type: 'line',  // Plot the trendline as a line chart
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    fill: false,
                    pointRadius: 0  // Hide the points on the trendline
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            tooltipFormat: 'yyyy-MM-dd',
                            displayFormats: {
                                day: 'yyyy-MM-dd'
                            }
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Engagement Volume'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return `(${tooltipItem.raw.x.toISOString().split('T')[0]}, ${tooltipItem.raw.y})`;
                            }
                        }
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching chart data:', error);
    });
}

let topThemesByPostVolChart;

function fetchTopThemesByPostVolData() {
    const filters = getFilters();

    fetch('/chart-data/top-themes-posts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: filters })
    })
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('topThemesByPostVolChart').getContext('2d');

        // Check if the chart already exists and destroy it before creating a new one
        if (topThemesByPostVolChart) {
            topThemesByPostVolChart.destroy();
        }

        topThemesByPostVolChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.themes,  // Themes returned from the backend
                datasets: [{
                    label: 'Post Volume',
                    data: data.post_counts,  // Post counts returned from the backend
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching chart data:', error);
    });
}

let topThemesByEngagementVolChart;

function fetchTopThemesByEngagementVolData() {
    const filters = getFilters();

    fetch('/chart-data/top-themes-engagements', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: filters })
    })
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('topThemesByEngagementVolChart').getContext('2d');

        // Check if the chart already exists and destroy it before creating a new one
        if (topThemesByEngagementVolChart) {
            topThemesByEngagementVolChart.destroy();
        }

        topThemesByEngagementVolChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.themes,  // Themes returned from the backend
                datasets: [{
                    label: 'Engagement Volume',
                    data: data.engagement_counts,  // Engagement counts returned from the backend
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching chart data:', error);
    });
}

let contentFormatsPostsChart;

function fetchContentFormatsPostsChartData() {
    const filters = getFilters();

    fetch('/chart-data/content-formats-posts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: filters })
    })
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('contentFormatsPostsChart').getContext('2d');

        if (contentFormatsPostsChart) {
            contentFormatsPostsChart.destroy();
        }
        
        contentFormatsPostsChart = new Chart(ctx, {
            type: 'bar',  // Change the chart type to 'bar'
            data: {
                labels: data.formats,  // The labels for the bar chart (content formats)
                datasets: [{
                    label: 'Content Formats',
                    data: data.format_counts,  // The data for each content format
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Content Formats'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Posts'
                        }
                    }
                },
                responsive: true,  // Allow the chart to be responsive
                plugins: {
                    legend: {
                        display: false  // Hide the legend if it's not needed
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return `${tooltipItem.raw} posts`;
                            }
                        }
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching chart data:', error);
    });
}

let contentFormatsEngagementsChart;

function fetchContentFormatsEngagementsChartData() {
    const filters = getFilters();

    fetch('/chart-data/content-formats-engagements', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: filters })
    })
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('contentFormatsEngagementsChart').getContext('2d');

        if (contentFormatsEngagementsChart) {
            contentFormatsEngagementsChart.destroy();
        }
        
        contentFormatsEngagementsChart = new Chart(ctx, {
            type: 'bar',  // Change the chart type to 'bar'
            data: {
                labels: data.formats,  // The labels for the bar chart (content formats)
                datasets: [{
                    label: 'Content Formats',
                    data: data.format_counts,  // The data for each content format
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Content Formats'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Engagements'
                        }
                    }
                },
                responsive: true,  // Allow the chart to be responsive
                plugins: {
                    legend: {
                        display: false  // Hide the legend if it's not needed
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return `${tooltipItem.raw} engagements`;
                            }
                        }
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching chart data:', error);
    });
}


function fetchTopExecutivesData() {
    const filters = getFilters();

    fetch('/chart-data/top-executives', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: filters })
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('topExecutivesTableBody');
        
        // Clear existing table rows
        tableBody.innerHTML = '';

        // Populate table with new data
        data.forEach((executive, index) => {
            const row = document.createElement('tr');

            const rankCell = document.createElement('td');
            rankCell.textContent = index + 1;
            row.appendChild(rankCell);

            const nameCell = document.createElement('td');
            const nameLink = document.createElement('a');
            nameLink.href = executive.profile_url;
            nameLink.textContent = executive.executive_name;
            nameLink.target = '_blank';
            nameCell.appendChild(nameLink);
            row.appendChild(nameCell);

            const postCountCell = document.createElement('td');
            postCountCell.textContent = executive.post_count;
            row.appendChild(postCountCell);

            const engagementCountCell = document.createElement('td');
            engagementCountCell.textContent = executive.engagement_count;
            row.appendChild(engagementCountCell);

            const totalCountCell = document.createElement('td');
            totalCountCell.textContent = executive.total_count;
            row.appendChild(totalCountCell);

            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error fetching table data:', error);
    });
}

function fetchTopPostsData() {
    const filters = getFilters();

    fetch('/chart-data/top-posts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters: filters })
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('topPostsTableBody');
        
        // Clear existing table rows
        tableBody.innerHTML = '';

        // Populate table with new data
        data.forEach((post, index) => {
            const row = document.createElement('tr');

            const rankCell = document.createElement('td');
            rankCell.textContent = index + 1;
            row.appendChild(rankCell);

            const nameCell = document.createElement('td');
            const nameLink = document.createElement('a');
            nameLink.href = post.profile_url;
            nameLink.textContent = post.executive_name;
            nameLink.target = '_blank';
            nameCell.appendChild(nameLink);
            row.appendChild(nameCell);

            const companyCell = document.createElement('td');
            companyCell.textContent = post.company;
            row.appendChild(companyCell);

            const industryCell = document.createElement('td');
            industryCell.textContent = post.industry;
            row.appendChild(industryCell);

            const themeCell = document.createElement('td');
            themeCell.textContent = post.theme;
            row.appendChild(themeCell);

            const contentCell = document.createElement('td');
            contentCell.textContent = post.post_content;
            row.appendChild(contentCell);

            const engagementCountCell = document.createElement('td');
            engagementCountCell.textContent = post.engagement_count;
            row.appendChild(engagementCountCell);

            const linkCell = document.createElement('td');
            const postLink = document.createElement('a');
            postLink.href = post.post_url;
            postLink.textContent = 'View Post';
            postLink.target = '_blank';
            linkCell.appendChild(postLink);
            row.appendChild(linkCell);

            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error fetching table data:', error);
    });
}

function searchPostContent() {
    const searchTerm = document.getElementById('searchInput').value.trim();

    fetch('/search-post-content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ searchTerm: searchTerm })
    })
    .then(response => response.json())
    .then(data => {
        const summaryData = data.summary_data;
        const posts = data.posts;
        const tableBody = document.getElementById('topPostsTableBody1');
        
        // Update summary cards
        document.getElementById('unique-audience-1').textContent = summaryData.unique_audience;
        document.getElementById('unique-posts-1').textContent = summaryData.total_posts;
        document.getElementById('total-engagements-1').textContent = summaryData.total_engagements;
        document.getElementById('average-engagements-1').textContent = summaryData.average_engagements;

        // Clear existing table rows
        tableBody.innerHTML = '';

        if (posts.length === 0) {
            const noResultsRow = document.createElement('tr');
            const noResultsCell = document.createElement('td');
            noResultsCell.textContent = 'No results found';
            noResultsCell.colSpan = 8;
            noResultsRow.appendChild(noResultsCell);
            tableBody.appendChild(noResultsRow);
        } else {
            posts.forEach((post, index) => {
                const row = document.createElement('tr');

                const rankCell = document.createElement('td');
                rankCell.textContent = index + 1;
                row.appendChild(rankCell);

                const nameCell = document.createElement('td');
                const nameLink = document.createElement('a');
                nameLink.href = post.profile_url;
                nameLink.textContent = post.executive_name;
                nameLink.target = '_blank';
                nameCell.appendChild(nameLink);
                row.appendChild(nameCell);

                const companyCell = document.createElement('td');
                companyCell.textContent = post.company;
                row.appendChild(companyCell);

                const industryCell = document.createElement('td');
                industryCell.textContent = post.industry;
                row.appendChild(industryCell);

                const themeCell = document.createElement('td');
                themeCell.textContent = post.theme;
                row.appendChild(themeCell);

                const contentCell = document.createElement('td');
                contentCell.textContent = post.post_content;
                row.appendChild(contentCell);

                const engagementCountCell = document.createElement('td');
                engagementCountCell.textContent = post.engagement_count;
                row.appendChild(engagementCountCell);

                const linkCell = document.createElement('td');
                const postLink = document.createElement('a');
                postLink.href = post.post_url;
                postLink.textContent = 'View Post';
                postLink.target = '_blank';
                linkCell.appendChild(postLink);
                row.appendChild(linkCell);

                tableBody.appendChild(row);
            });
        }
    })
    .catch(error => {
        console.error('Error fetching search results:', error);
    });
}
