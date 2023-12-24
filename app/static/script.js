var userFromDataAttribute = document
  .getElementById("container")
  .getAttribute("data-user");

console.log(userFromDataAttribute);

document.addEventListener("DOMContentLoaded", function () {
  let chart;
  let chartData = [];

  function initializeChart(data) {
    chartData = JSON.parse(data);

    chartData.forEach(function (item) {
      var date = new Date(item.x * 1000);
      var timeString = date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        timeZone: "UTC",
      });
      item.x = timeString;
    });

    chart = Highcharts.chart("containerconc", {
      chart: {
        type: "line",
      },
      title: {
        text: "Concentration",
      },
      xAxis: {
        type: "category",
        title: {
          text: "Date",
        },
        categories: chartData.map((item) => item.x),
      },
      yAxis: {
        title: {
          text: "Concentration",
        },
      },
      scrollbar: {
        enabled: true,
      },
      series: [
        {
          name: "Concentration",
          data: chartData.map((item) => item.y),
          turboThreshold: 1000,
          color: "orange",
          dataGrouping: {
            enabled: true,
            approximation: "average",
            forced: true,
            units: [["day", [1]]],
          },
        },
      ],
    });
  }

  async function fetchData() {
    try {
      let response = await fetch(
        `http://localhost:5000/upl?user_id=${userFromDataAttribute}`
      );

      if (response.ok) {
        let json = await response.json();
        console.log(json);

        if (!chart) {
          initializeChart(JSON.stringify(json));
        } else {
          chartData = JSON.parse(JSON.stringify(json));
          chartData.forEach(function (item) {
            var date = new Date(item.x * 1000);
            var timeString = date.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
              timeZone: "UTC", // Измененный формат времени для концентрации
            });
            item.x = timeString;
          });

          chart.series[0].setData(
            chartData.map((item) => item.y),
            false
          );
          chart.xAxis[0].setCategories(chartData.map((item) => item.x));
          chart.redraw();
        }
      } else {
        console.log("Ошибка HTTP: " + response.status);
      }
    } catch (error) {
      console.log("Произошла ошибка:", error);
    }
  }

  setInterval(fetchData, 1000);

  let chartRelax;
  let chartDataRelax = [];

  function initializeChartRelax(data) {
    chartDataRelax = JSON.parse(data);

    chartDataRelax.forEach(function (item) {
      var date = new Date(item.x * 1000);
      var timeString = date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
      item.x = timeString;
    });

    chartRelax = Highcharts.chart("containerrelax", {
      chart: {
        type: "line",
      },
      title: {
        text: "Relax",
      },
      xAxis: {
        type: "category",
        title: {
          text: "Date",
        },
        categories: chartDataRelax.map((item) => item.x),
      },
      yAxis: {
        title: {
          text: "Relax",
        },
      },
      scrollbar: {
        enabled: true,
      },
      series: [
        {
          name: "Relax",
          data: chartDataRelax.map((item) => item.y),
          turboThreshold: 1000,
          color: "green",
          dataGrouping: {
            enabled: true,
            approximation: "average",
            forced: true,
            units: [["day", [1]]],
          },
        },
      ],
    });
  }

  async function fetchDataRelax() {
    try {
      let response = await fetch(
        `http://localhost:5000/uplrelax?user_id=${userFromDataAttribute}`
      );

      if (response.ok) {
        let json = await response.json();
        console.log(json);

        if (!chartRelax) {
          initializeChartRelax(JSON.stringify(json));
        } else {
          chartDataRelax = JSON.parse(JSON.stringify(json));
          chartDataRelax.forEach(function (item) {
            var date = new Date(item.x * 1000);
            var timeString = date.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
            });
            item.x = timeString;
          });

          chartRelax.series[0].setData(
            chartDataRelax.map((item) => item.y),
            false
          );
          chartRelax.xAxis[0].setCategories(
            chartDataRelax.map((item) => item.x)
          );
          chartRelax.redraw();
        }
      } else {
        console.log("Ошибка HTTP: " + response.status);
      }
    } catch (error) {
      console.log("Произошла ошибка:", error);
    }
  }

  setInterval(fetchDataRelax, 1000);
});
