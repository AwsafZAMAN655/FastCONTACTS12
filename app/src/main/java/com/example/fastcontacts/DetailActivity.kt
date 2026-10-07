package com.example.fastcontacts

import android.graphics.Color
import android.graphics.Typeface
import android.os.Bundle
import android.view.Gravity
import android.view.LayoutInflater
import android.view.View
import android.widget.Button
import android.widget.GridLayout
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class DetailActivity : AppCompatActivity() {

    private var contactId = -1L
    private var contact: Contact? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_detail)
        contactId = intent.getLongExtra("contact_id", -1L)

        findViewById<Button>(R.id.btnCallAction).setOnClickListener {
            contact?.let { c -> Actions.withNumber(this, c) { n -> Actions.call(this, n) } }
        }
        findViewById<Button>(R.id.btnSmsAction).setOnClickListener {
            contact?.let { c -> Actions.withNumber(this, c) { n -> Actions.sms(this, n) } }
        }
        findViewById<Button>(R.id.btnWhatsAppAction).setOnClickListener {
            contact?.let { c ->
                Actions.withNumber(this, c) { n -> Actions.openSocial(this, Social.whatsapp, n) }
            }
        }
        findViewById<Button>(R.id.btnEmailAction).setOnClickListener {
            contact?.let { c -> Actions.withEmail(this, c) { e -> Actions.email(this, e) } }
        }
        findViewById<Button>(R.id.btnFavAction).setOnClickListener {
            contact?.let { c ->
                Actions.toggleStar(this, c)
                load()
            }
        }
        findViewById<Button>(R.id.btnEditAction).setOnClickListener {
            contact?.let { c -> Actions.edit(this, c) }
        }
        findViewById<Button>(R.id.btnDeleteAction).setOnClickListener {
            contact?.let { c -> Actions.confirmDelete(this, c) { finish() } }
        }
    }

    override fun onResume() {
        super.onResume()
        load()
    }

    private fun load() {
        Thread {
            val c = ContactsRepository.loadById(this, contactId)
            runOnUiThread {
                if (c == null) {
                    finish()
                } else {
                    contact = c
                    bind(c)
                }
            }
        }.start()
    }

    private fun dp(v: Int): Int = (v * resources.displayMetrics.density).toInt()

    private fun bind(c: Contact) {
        val avatar = findViewById<TextView>(R.id.detailAvatar)
        avatar.text = Avatar.letter(c.name)
        avatar.background = Avatar.circle(c.name)

        findViewById<TextView>(R.id.detailName).text = c.name
        findViewById<TextView>(R.id.detailPhone).text = when (c.phones.size) {
            0 -> "No phone number"
            1 -> c.phones[0].number
            else -> c.phones.size.toString() + " phone numbers"
        }
        findViewById<TextView>(R.id.detailEmail).text = c.emails.firstOrNull()?.address ?: ""
        findViewById<Button>(R.id.btnFavAction).text = if (c.starred) "Unfavorite" else "Favorite"

        val phones = findViewById<LinearLayout>(R.id.phonesContainer)
        phones.removeAllViews()
        val inflater = LayoutInflater.from(this)
        for (p in c.phones) {
            val row = inflater.inflate(R.layout.row_phone, phones, false)
            row.findViewById<TextView>(R.id.rowNumber).text = p.number
            row.findViewById<TextView>(R.id.rowType).text = p.type
            val wa = row.findViewById<TextView>(R.id.rowWa)
            wa.background = Avatar.solidCircle(Social.whatsapp.color)
            wa.setOnClickListener { Actions.openSocial(this, Social.whatsapp, p.number) }
            row.findViewById<ImageButton>(R.id.rowSms).setOnClickListener { Actions.sms(this, p.number) }
            row.findViewById<ImageButton>(R.id.rowCall).setOnClickListener { Actions.call(this, p.number) }
            phones.addView(row)
        }

        val emails = findViewById<LinearLayout>(R.id.emailsContainer)
        emails.removeAllViews()
        findViewById<View>(R.id.emailsTitle).visibility = if (c.emails.isEmpty()) View.GONE else View.VISIBLE
        for (e in c.emails) {
            val row = inflater.inflate(R.layout.row_email, emails, false)
            row.findViewById<TextView>(R.id.emailAddr).text = e.address
            row.findViewById<TextView>(R.id.emailType).text = e.type
            row.setOnClickListener { Actions.email(this, e.address) }
            emails.addView(row)
        }

        buildSocialGrid(c)
    }

    private fun buildSocialGrid(c: Contact) {
        val grid = findViewById<GridLayout>(R.id.socialGrid)
        grid.removeAllViews()
        for (app in Social.apps) {
            val cell = LinearLayout(this)
            cell.orientation = LinearLayout.VERTICAL
            cell.gravity = Gravity.CENTER
            cell.setPadding(0, dp(8), 0, dp(8))

            val circle = TextView(this)
            circle.text = app.short
            circle.gravity = Gravity.CENTER
            circle.setTextColor(Color.WHITE)
            circle.textSize = 14f
            circle.setTypeface(null, Typeface.BOLD)
            circle.background = Avatar.solidCircle(app.color)
            circle.layoutParams = LinearLayout.LayoutParams(dp(48), dp(48))

            val label = TextView(this)
            label.text = app.label
            label.textSize = 11f
            label.gravity = Gravity.CENTER
            label.setPadding(0, dp(4), 0, 0)

            cell.addView(circle)
            cell.addView(label)
            cell.alpha = if (Actions.isInstalled(this, app)) 1f else 0.35f
            cell.setOnClickListener {
                Actions.withNumber(this, c) { n -> Actions.openSocial(this, app, n) }
            }

            val lp = GridLayout.LayoutParams(
                GridLayout.spec(GridLayout.UNDEFINED),
                GridLayout.spec(GridLayout.UNDEFINED, 1f)
            )
            lp.width = 0
            grid.addView(cell, lp)
        }
    }
}
