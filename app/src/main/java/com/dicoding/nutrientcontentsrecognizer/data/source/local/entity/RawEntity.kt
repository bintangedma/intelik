package com.dicoding.nutrientcontentsrecognizer.data.source.local.entity

import android.graphics.Bitmap
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "tb_plants")
data class RawEntity(
    @PrimaryKey(autoGenerate = true)
    val calcium_mg: Int = 0,
    val carb_g: Float,
    val copper_mcg: Float,
    val date: String,
    val img: Bitmap
)