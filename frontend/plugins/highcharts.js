import Vue from 'vue'
import Highcharts from 'highcharts'
import HighchartsVue from 'highcharts-vue'
import stockInit from 'highcharts/modules/stock'

if (typeof Highcharts === 'object') {
  stockInit(Highcharts)
}

Vue.use(HighchartsVue)
