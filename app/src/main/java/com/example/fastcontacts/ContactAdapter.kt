package com.example.fastcontacts

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageButton
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class ContactAdapter(
    private val onClick: (Contact) -> Unit,
    private val onCallClick: (Contact) -> Unit,
    private val onSmsClick: (Contact) -> Unit,
    private val onLongClick: (Contact) -> Unit = {},
    private val onFavClick: (Contact) -> Unit = {}
) : RecyclerView.Adapter<RecyclerView.ViewHolder>() {

    private sealed class Row {
        class Header(val letter: String) : Row()
        class Item(val contact: Contact) : Row()
    }

    private var rows: List<Row> = emptyList()
    private var showEmail = true

    fun submit(
        list: List<Contact>,
        showHeaders: Boolean = false,
        showEmail: Boolean = true,
        byLast: Boolean = false
    ) {
        this.showEmail = showEmail
        val out = ArrayList<Row>()
        var lastLetter = ""
        for (c in list) {
            if (showHeaders) {
                val letter = SearchEngine.letterOf(c, byLast)
                if (letter != lastLetter) {
                    out.add(Row.Header(letter))
                    lastLetter = letter
                }
            }
            out.add(Row.Item(c))
        }
        rows = out
        notifyDataSetChanged()
    }

    override fun getItemViewType(position: Int): Int =
        if (rows[position] is Row.Header) 0 else 1

    override fun getItemCount(): Int = rows.size

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        return if (viewType == 0) {
            HeaderVH(inflater.inflate(R.layout.item_header, parent, false))
        } else {
            VH(inflater.inflate(R.layout.item_contact, parent, false))
        }
    }

    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        val row = rows[position]
        if (holder is HeaderVH && row is Row.Header) {
            holder.text.text = row.letter
            return
        }
        if (holder !is VH || row !is Row.Item) return

        val c = row.contact
        holder.name.text = c.name

        val first = c.phones.firstOrNull()?.number ?: "No phone number"
        holder.number.text = if (c.phones.size > 1) first + "  (+" + (c.phones.size - 1) + " more)" else first

        holder.avatar.text = Avatar.letter(c.name)
        holder.avatar.background = Avatar.circle(c.name)

        val email = c.emails.firstOrNull()?.address
        if (showEmail && !email.isNullOrEmpty()) {
            holder.email.text = email
            holder.email.visibility = View.VISIBLE
        } else {
            holder.email.visibility = View.GONE
        }

        holder.fav.setImageResource(
            if (c.starred) android.R.drawable.btn_star_big_on else android.R.drawable.btn_star_big_off
        )

        holder.itemView.setOnClickListener { onClick(c) }
        holder.itemView.setOnLongClickListener { onLongClick(c); true }
        holder.btnCall.setOnClickListener { onCallClick(c) }
        holder.btnSms.setOnClickListener { onSmsClick(c) }
        holder.fav.setOnClickListener { onFavClick(c) }
    }

    class VH(view: View) : RecyclerView.ViewHolder(view) {
        val avatar: TextView = view.findViewById(R.id.avatar)
        val name: TextView = view.findViewById(R.id.name)
        val number: TextView = view.findViewById(R.id.number)
        val email: TextView = view.findViewById(R.id.email)
        val btnCall: ImageButton = view.findViewById(R.id.btnCall)
        val btnSms: ImageButton = view.findViewById(R.id.btnSms)
        val fav: ImageButton = view.findViewById(R.id.btnFav)
    }

    class HeaderVH(view: View) : RecyclerView.ViewHolder(view) {
        val text: TextView = view.findViewById(R.id.headerText)
    }
}
