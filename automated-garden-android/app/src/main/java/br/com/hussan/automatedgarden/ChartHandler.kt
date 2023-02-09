package br.com.hussan.automatedgarden

import android.content.Context
import android.util.Log
import androidx.core.content.ContextCompat
import br.com.hussan.automatedgarden.model.SensorValue
import com.github.mikephil.charting.charts.LineChart
import com.github.mikephil.charting.components.Description
import com.github.mikephil.charting.components.XAxis
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.LineData
import com.github.mikephil.charting.data.LineDataSet
import com.github.mikephil.charting.formatter.IAxisValueFormatter
import com.google.firebase.firestore.QueryDocumentSnapshot
import com.google.firebase.firestore.QuerySnapshot
import com.google.firebase.firestore.ktx.toObject
import java.time.Instant
import java.time.ZoneId

object ChartHandler {
    fun plot(
        context: Context,
        result: List<QueryDocumentSnapshot>?,
        label: String,
        chart: LineChart
    ) {
        val entries = ArrayList<Entry>()
        result?.forEachIndexed { index, document ->
            val sensorValue = document.toObject<SensorValue>()
            Log.d("h2", sensorValue.toString())
            entries.add(Entry(index.toFloat(), sensorValue.value.toFloat()))
        }

        val dataSetMax = LineDataSet(entries, label).apply {
            color = ContextCompat.getColor(context, R.color.black)
            setCircleColor(color)
            setDrawValues(false)
        }

        val lineData = LineData(listOf(dataSetMax))
        chart.apply {
            data = lineData
            description = Description().apply { text = "" }

            axisLeft.apply {
                textSize = 11f
            }
            axisRight.apply {
                isEnabled = false
            }
//            xAxis.apply {
//                isEnabled = false
//                position = XAxis.XAxisPosition.BOTTOM
//                labelRotationAngle = -25f
//                textSize = 10f
//                valueFormatter = IAxisValueFormatter { value, axis ->
//                    try {
//                        result?.date(value.toInt())
//                    } catch (e: IndexOutOfBoundsException) {
//                        ""
//                    }
//                }
//            }

            invalidate()
        }
    }
}

fun QuerySnapshot.date(index: Int): String {
    val sensorValue = this.toList()[index].toObject<SensorValue>()
    val dt = Instant.ofEpochSecond(sensorValue.timestamp ?: 0L)
        .atZone(ZoneId.systemDefault())
        .toLocalDateTime()
    return dt.toString()
}
