import Vue from 'vue'
import Highcharts from 'highcharts'
import WindbarbHighcharts from 'highcharts/modules/windbarb'
import HighchartsVue from 'highcharts-vue'

if (typeof Highcharts === 'object') {
  WindbarbHighcharts(Highcharts)
}

Vue.use(HighchartsVue)
