package br.com.hussan.automatedgarden

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.Menu
import android.view.MenuInflater
import android.view.MenuItem
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import androidx.appcompat.app.AppCompatActivity
import br.com.hussan.automatedgarden.databinding.ActivityMainBinding
import br.com.hussan.automatedgarden.model.Preset
import br.com.hussan.automatedgarden.model.Sensor
import br.com.hussan.automatedgarden.model.SensorValue
import br.com.hussan.automatedgarden.model.Sensors
import com.github.mikephil.charting.charts.LineChart
import com.google.firebase.firestore.QuerySnapshot
import com.google.firebase.firestore.ktx.toObject
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import org.eclipse.paho.client.mqttv3.MqttMessage


class MainActivity : AppCompatActivity() {

    private val mqttClient = MqttClient(::onMessageArrived)
    private val fireStore = FireStore()
    private lateinit var binding: ActivityMainBinding
    private var switchWater = false
    private val sensors by lazy {
        Sensors(binding)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        val view = binding.root
        binding.swiperefresh.setOnRefreshListener {
            getData()
        }
        binding.switchWater.setOnCheckedChangeListener { _, isChecked ->
            if(isChecked) {
                mqttClient.publish(Config.topics.last(), "on")
            } else {
                mqttClient.publish(Config.topics.last(), "off")
            }
            switchWater = true
        }
        setContentView(view)
    }

    override fun onResume() {
        super.onResume()
        getData()

        mqttClient.run {
            connect(this@MainActivity, ::onConnectionSuccess, ::onConnectionFailure)
        }
    }

    private fun getData() {
        sensors.sensors.forEach {
            fireStore.get(it.collection) { result ->
                plotChart(result, it.chartView, it.name)
            }
        }

        fireStore.get(Config.presetCollection, limit = 1) { result ->
            result?.forEachIndexed { index, document ->
                val preset = document.toObject<Preset>()
                binding.txtPresetTime1.text = preset.time1
                binding.txtPresetTime2.text = preset.time2
                binding.txtPresetHumidity.text = preset.soilHumidity
                Log.d("h2", "preset: $preset")
                Log.d("h2", "preset: $document.id")
            }
        }
        binding.swiperefresh.isRefreshing = false
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        val inflater: MenuInflater = menuInflater
        inflater.inflate(R.menu.menu, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle item selection
        return when (item.itemId) {
            R.id.new_preset -> {
                startActivity(Intent(this, PresetActivity::class.java))
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    private fun plotChart(
        result: QuerySnapshot?,
        chartView: LineChart,
        label: String
    ) {
        if (result != null) {
            ChartHandler.plot(this, result.reversed(), label, chartView)
        }
    }

    @SuppressLint("SetTextI18n")
    private fun onMessageArrived(topic: String, message: MqttMessage) {
        val data = String(message.payload, charset("UTF-8"))

        Log.i("h2", "topic: $topic - message: $data")

        val startAnimation: Animation = AnimationUtils.loadAnimation(this, R.anim.blink)

        if (topic == Config.topics[4]) {
            binding.switchWater.isChecked = data == "on"
        } else {
            val sensorValue = Json.decodeFromString<SensorValue>(data)

            when (topic) {
                sensors.soilSensor.topic -> {
                    binding.cardView1.startAnimation(startAnimation)
                    binding.txtSoil.text = "${sensorValue.value}%"
                }
                sensors.tempSensor.topic -> {
                    binding.cardView2.startAnimation(startAnimation)
                    binding.txtTempAir.text = "${sensorValue.value}°"
                }
                sensors.humiditySensor.topic -> {
                    binding.cardView3.startAnimation(startAnimation)
                    binding.txtHumidityAir.text = "${sensorValue.value}%"
                }
                sensors.rainSensor.topic -> {
                    binding.cardView4.startAnimation(startAnimation)
                    binding.txtRain.text = "${sensorValue.value}%"
                }
            }
        }

    }

    private fun onSubscriptionFailure() { Log.i("h2", "onSubscriptionFailure ") }

    private fun onSubscriptionSuccess() {
        Log.i("h2", "onSubscriptionSuccess ")
        mqttClient.receiveMessages()
    }

    private fun onConnectionFailure() { Log.i("h2", "onConnectionFailure ") }

    private fun onConnectionSuccess() {
        Log.i("h2", "onConnectionSuccess ")
        mqttClient.subscribe(Config.topics, Config.qos, ::onSubscriptionSuccess, ::onSubscriptionFailure)
    }

    override fun onPause() {
        super.onPause()
        mqttClient.disconnect()
    }
}