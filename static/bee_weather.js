document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('toggle-table');
    const dataContainer = document.getElementById('data-container');
  
    toggleBtn.addEventListener('click', () => {
      const isVisible = dataContainer.style.display !== 'none';
      dataContainer.style.display = isVisible ? 'none' : 'block';
      toggleBtn.textContent = isVisible ? 'Show Weather Data' : 'Hide Weather Data';
    });
  
    fetch('/bee_activity_forecast.csv')
      .then(response => response.text())
      .then(text => {
        const rows = text.trim().split('\n');
        let html = '<table><tr>';
        const headers = rows[0].split(',');
  
        headers.forEach(h => html += `<th>${h}</th>`);
        html += '</tr>';
  
        for (let i = 1; i < rows.length; i++) {
          const cols = rows[i].split(',');
          html += '<tr>';
          cols.forEach((c, j) => {
            let bg = '';
            if (j === 4) {
              const val = c.trim();
              if (val === 'Optimal') bg = 'style="background:#a1d99b"';
              else if (val === 'Moderate') bg = 'style="background:#fdae6b"';
              else if (val === 'Low') bg = 'style="background:#fb6a4a"';
            }
            html += `<td ${bg}>${c}</td>`;
          });
          html += '</tr>';
        }
  
        html += '</table>';
        document.getElementById('data-table').innerHTML = html;
      })
      .catch(err => {
        document.getElementById('data-table').innerHTML = 'Failed to load weather data.';
        console.error('Error loading weather data:', err);
      });
  });

  window.addEventListener('load', () => {
    const container = document.getElementById('weather-table-container');
    container.style.maxHeight = (window.innerHeight - 100) + 'px';
  });

document.getElementById('toggle-marker').addEventListener('click', function() {
    markerMode = !markerMode;
    this.textContent = "Marker Mode: " + (markerMode ? "ON" : "OFF");
  });
  
  