package com.dicoding.nutrientcontentsrecognizer.ui.notifications

import android.Manifest
import android.app.Activity
import android.app.Activity.RESULT_OK
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.MediaStore
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageButton
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import com.dicoding.nutrientcontentsrecognizer.MediaStoreUtils
import com.dicoding.nutrientcontentsrecognizer.R
import com.dicoding.nutrientcontentsrecognizer.databinding.FragmentCameraBinding
import com.dicoding.nutrientcontentsrecognizer.databinding.FragmentGalleryBinding
import kotlinx.android.synthetic.main.fragment_gallery.*
import java.io.File
import java.io.FileInputStream
import java.io.IOException
import java.text.DecimalFormat

class GalleryFragment : Fragment() {
    private lateinit var fragmentGalleryBinding: FragmentGalleryBinding

    private val pickImage = 100
    private var imageUri: Uri? = null

    override fun onCreateView(
            inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View?
    {
        fragmentGalleryBinding = FragmentGalleryBinding.inflate(layoutInflater, container, false)
        return fragmentGalleryBinding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        image_button.setOnClickListener {
            val gallery = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.INTERNAL_CONTENT_URI)
            startActivityForResult(gallery, pickImage)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode == RESULT_OK && requestCode == pickImage) {
            imageUri = data?.data
            image_view.setImageURI(imageUri)
        }
    }

}
