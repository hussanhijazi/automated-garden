package br.com.hussan.automatedgarden.model

import kotlinx.serialization.Serializable

@Serializable
data class SensorValue(val value: String = "", val timestamp: Long? = 0L)
