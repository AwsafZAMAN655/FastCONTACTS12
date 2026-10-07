package com.example.fastcontacts

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.TextView
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.widget.doAfterTextChanged
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButtonToggleGroup
import com.google.android.material.floatingactionbutton.FloatingActionButton

class MainActivity : AppCompatActivity() {

    private lateinit var adapter: ContactAdapter
    private lateinit var search: EditText
    private lateinit var btnClear: ImageButton
    private lateinit var emptyState: View
    private lateinit var tvCount: TextView
    private lateinit var permissionPanel: View
    private lateinit var toggleGroup: MaterialButtonToggleGroup

    private var sortedAll: List<Contact> = emptyList()
    private var favoritesOnly = false

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) {
        if (hasContactsPermission()) loadContacts() else showPermissionPanel()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        search = findViewById(R.id.search)
        btnClear = findViewById(R.id.btnClearSearch)
        emptyState = findViewById(R.id.emptyState)
        tvCount = findViewById(R.id.tvCount)
        permissionPanel = findViewById(R.id.permissionPanel)
        toggleGroup = findViewById(R.id.toggleGroup)
        val list = findViewById<RecyclerView>(R.id.list)

        adapter = ContactAdapter(
            onClick = { openDetail(it) },
            onCallClick = { c -> Actions.withNumber(this, c) { n -> Actions.call(this, n) } },
            onSmsClick = { c -> Actions.withNumber(this, c) { n -> Actions.sms(this, n) } },
            onLongClick = { showQuickMenu(it) },
            onFavClick = { c ->
                Actions.toggleStar(this, c)
                loadContacts()
            }
        )
        list.layoutManager = LinearLayoutManager(this)
        list.adapter = adapter

        search.doAfterTextChanged {
            btnClear.visibility = if (it.isNullOrEmpty()) View.GONE else View.VISIBLE
            applyFilter()
        }
        btnClear.setOnClickListener { search.setText("") }

        findViewById<ImageButton>(R.id.btnSettings).setOnClickListener {
            startActivity(Intent(this, SettingsActivity::class.java))
        }
        findViewById<FloatingActionButton>(R.id.fabDialpad).setOnClickListener {
            startActivity(Intent(this, DialpadActivity::class.java))
        }
        findViewById<Button>(R.id.permissionButton).setOnClickListener { requestPermissions() }

        toggleGroup.check(R.id.btnAll)
        toggleGroup.addOnButtonCheckedListener { _, checkedId, isChecked ->
            if (isChecked) {
                favoritesOnly = checkedId == R.id.btnFavorites
                applyFilter()
            }
        }

        if (!hasContactsPermission()) requestPermissions()
    }

    override fun onResume() {
        super.onResume()
        if (hasContactsPermission()) loadContacts()
    }

    private fun hasContactsPermission(): Boolean =
        ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) ==
            PackageManager.PERMISSION_GRANTED

    private fun requestPermissions() {
        permissionLauncher.launch(
            arrayOf(
                Manifest.permission.READ_CONTACTS,
                Manifest.permission.WRITE_CONTACTS,
                Manifest.permission.CALL_PHONE
            )
        )
    }

    private fun showPermissionPanel() {
        permissionPanel.visibility = View.VISIBLE
        emptyState.visibility = View.GONE
    }

    private fun loadContacts() {
        permissionPanel.visibility = View.GONE
        Thread {
            val loaded = ContactsRepository.loadAll(this)
            val sorted = SearchEngine.sorted(loaded, Prefs.sortByLast(this))
            runOnUiThread {
                sortedAll = sorted
                applyFilter()
            }
        }.start()
    }

    private fun applyFilter() {
        val q = search.text.toString()
        val base = if (favoritesOnly) sortedAll.filter { it.starred } else sortedAll
        val result = SearchEngine(base).search(q)
        adapter.submit(result, q.isBlank(), Prefs.showEmail(this), Prefs.sortByLast(this))
        emptyState.visibility =
            if (result.isEmpty() && permissionPanel.visibility != View.VISIBLE) View.VISIBLE else View.GONE
        tvCount.text = result.size.toString() + " contacts"
    }

    private fun openDetail(c: Contact) {
        val i = Intent(this, DetailActivity::class.java)
        i.putExtra("contact_id", c.id)
        startActivity(i)
    }

    private fun showQuickMenu(c: Contact) {
        val star = if (c.starred) "Remove from favorites" else "Add to favorites"
        val items = arrayOf("Call", "SMS", "WhatsApp", star, "Edit contact", "Delete contact")
        AlertDialog.Builder(this)
            .setTitle(c.name)
            .setItems(items) { _, which ->
                when (which) {
                    0 -> Actions.withNumber(this, c) { n -> Actions.call(this, n) }
                    1 -> Actions.withNumber(this, c) { n -> Actions.sms(this, n) }
                    2 -> Actions.withNumber(this, c) { n -> Actions.openSocial(this, Social.whatsapp, n) }
                    3 -> {
                        Actions.toggleStar(this, c)
                        loadContacts()
                    }
                    4 -> Actions.edit(this, c)
                    5 -> Actions.confirmDelete(this, c) { loadContacts() }
                }
            }
            .show()
    }
}
