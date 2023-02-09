package br.com.hussan.automatedgarden

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import br.com.hussan.automatedgarden.databinding.ActivityPresetBinding
import com.google.firebase.firestore.FieldValue
import com.google.firebase.firestore.model.FieldPath

class PresetActivity : AppCompatActivity() {

    private lateinit var binding: ActivityPresetBinding
    private val fireStore = FireStore()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityPresetBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)
        binding.buttonAdd.setOnClickListener {
            val data = mapOf(
                "time1" to binding.txtTime1.text.toString(),
                "time2" to binding.txtTime2.text.toString(),
                "soilHumidity" to binding.txtHumidity.text.toString(),
                "timestamp" to FieldValue.serverTimestamp()
            )
            fireStore.add(
                Config.presetCollection,
                data
            ) {
                Toast.makeText(this, "Preset Adicionado com sucesso...", Toast.LENGTH_LONG).show()
                finish()
            }
        }
    }
}