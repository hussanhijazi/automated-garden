package br.com.hussan.automatedgarden.model

import com.github.mikephil.charting.charts.LineChart

data class Sensor(
    val name: String,
    val topic: String,
    val collection: String,
    val chartView: LineChart
)