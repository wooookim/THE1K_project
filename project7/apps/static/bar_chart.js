new Chart(document.getElementById("bar-chart-1"),{
    type: 'bar',
    data: {
        labels: ["0", "1", "2", "3", "4", "5"],
        datasets: [
            // {
            //     label: "공부 시간(분)",
            //     backgroundColor: "#3e95cd",
            //     data: [60, 60, 60, 34, 0, 0]
            // },
            {
                label: "집중 시간(분)",
                backgroundColor: "#3e95cd",
                data: [23, 34, 45, 23, 29, 52]
            }
        ]
        
    },
    options: {
        legend: { display: false },
        title: {
          display: true,
          text: '오늘 집중 시간'
        },
        scales: {
            x: {
                min: 0,
                max: 23
            },
            y: {
                min:0,
                max: 60
            }
        },
      }
})

// new Chart(document.getElementById("bar-chart-2"),{
//     type: 'bar',
//     data: {
//         labels: ["0", "1", "2", "3", "4", "5"],
//         datasets: [
//             // {
//             //     label: "공부 시간(분)",
//             //     backgroundColor: "#3e95cd",
//             //     data: [60, 60, 60, 34, 0, 0]
//             // },
//             {
//                 label: "순 공부 시간(분)",
//                 backgroundColor: "#3e95cd",
//                 data: [30, 23, 43, 50, 23, 0]
//             }
//         ]
        
//     },
//     options: {
//         legend: { display: false },
//         title: {
//           display: true,
//           text: '오늘 집중 시간'
//         },
//         scales: {
//             x: {
//                 min: 0,
//                 max: 23
//             },
//             y: {
//                 min:0,
//                 max: 60
//             }
//         },
//       }
// })

new Chart(document.getElementById("bar-chart-3"),{
    type: 'bar',
    data: {
        labels: ["일", "월", "화", "수", "목", "금", "토"],
        datasets: [
            {
                label: "공부 시간",
                backgroundColor: "#3e95cd",
                data: [148, 0, 283, 345, 250, 230, 160]
            },
            {
                label: "집중 시간(분)",
                backgroundColor: "#3e9534",
                data: [100, 0, 183, 250, 230, 192, 103]
            }
        ]
        
    },
    options: {
        legend: { display: true },
        title: {
          display: true,
          text: '이번주 공부'
        }
      }
})