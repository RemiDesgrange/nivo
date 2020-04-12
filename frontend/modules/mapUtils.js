import Style from 'ol/style/Style'
import Fill from 'ol/style/Fill'
import Stroke from 'ol/style/Stroke'

export function selectionStyleBasedOnExisting(feature) {
  // takes an existing styles and make it sligthly bigger when selected.
  const existingStyle = feature.getStyle()
  if (existingStyle instanceof Style) {
    const stroke = existingStyle.getStroke()
    stroke.setWidth(stroke.getWidth() + 3)
    return new Style({
      stroke,
      fill: existingStyle.getFill(),
    })
  }
}

function _setOpacityInRGBA(color, opacity) {
  const newcol = color.split(',')
  newcol.pop()
  newcol.push(` ${opacity})`)
  return newcol.join(',')
}

export function massifsStyleFunc(feature) {
  const risk = feature.get('lastest_risk')
  const color = {
    '5': 'rgba(254, 5, 0, 1)',
    '4': 'rgba(254, 5, 0, 1)',
    '3': 'rgba(255, 158, 1, 1)',
    '2': 'rgba(254, 255, 0, 1)',
    '1': 'rgba(205, 255, 96, 1)',
  }
  const index = Object.keys(color).find((e) => Number(e) === risk)
  let currentRiskColor = null
  if (index === undefined) {
    currentRiskColor = 'rgba(86, 130, 243, 1)'
  } else {
    currentRiskColor = color[index]
  }

  return new Style({
    fill: new Fill({
      color: _setOpacityInRGBA(currentRiskColor, 0.3),
    }),
    stroke: new Stroke({
      color: currentRiskColor,
      width: 2,
    }),
  })
}
