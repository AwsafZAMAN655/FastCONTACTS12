package com.example.fastcontacts

import android.Manifest
import android.app.Activity
import android.content.ClipData
import android.content.ClipboardManager
import android.content.ContentUris
import android.content.ContentValues
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.drawable.GradientDrawable
import android.net.Uri
import android.provider.ContactsContract
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.core.content.ContextCompat

data class SocialApp(
    val label: String,
    val short: String,
    val color: Int,
    val pkg: String,
    val link: ((String) -> String)? = null
)

object Social {
    val whatsapp = SocialApp("WhatsApp", "WA", 0xFF25D366.toInt(), "com.whatsapp") { n -> "https://wa.me/" + n }

    val apps: List<SocialApp> = listOf(
        whatsapp,
        SocialApp("WA Business", "WB", 0xFF128C7E.toInt(), "com.whatsapp.w4b") { n -> "https://wa.me/" + n },
        SocialApp("imo", "imo", 0xFF1D9BF0.toInt(), "com.imo.android.imoim"),
        SocialApp("Telegram", "TG", 0xFF229ED9.toInt(), "org.telegram.messenger") { n -> "https://t.me/+" + n },
        SocialApp("Viber", "Vb", 0xFF7360F2.toInt(), "com.viber.voip") { n -> "viber://chat?number=%2B" + n },
        SocialApp("Signal", "Sg", 0xFF3A76F0.toInt(), "org.thoughtcrime.securesms") { n -> "sgnl://signal.me/#p/+" + n },
        SocialApp("Messenger", "Ms", 0xFF0084FF.toInt(), "com.facebook.orca"),
        SocialApp("Facebook", "Fb", 0xFF1877F2.toInt(), "com.facebook.katana"),
        SocialApp("Instagram", "Ig", 0xFFC13584.toInt(), "com.instagram.android"),
        SocialApp("Skype", "Sk", 0xFF00AFF0.toInt(), "com.skype.raider") { n -> "skype:" + n + "?chat" },
        SocialApp("Snapchat", "Sc", 0xFFF2C500.toInt(), "com.snapchat.android"),
        SocialApp("Meet", "Mt", 0xFF00897B.toInt(), "com.google.android.apps.tachyon")
    )
}

object Avatar {
    private val colors = intArrayOf(
        0xFF1A73E8.toInt(), 0xFFEA4335.toInt(), 0xFF34A853.toInt(), 0xFFF29900.toInt(),
        0xFF9334E6.toInt(), 0xFF129EAF.toInt(), 0xFFE8710A.toInt(), 0xFFD01884.toInt(),
        0xFF5F6368.toInt()
    )

    fun letter(name: String): String = name.trim().firstOrNull()?.uppercase() ?: "?"

    fun solidCircle(color: Int): GradientDrawable {
        val d = GradientDrawable()
        d.shape = GradientDrawable.OVAL
        d.setColor(color)
        return d
    }

    fun circle(name: String): GradientDrawable {
        val idx = (name.hashCode() and 0x7fffffff) % colors.size
        return solidCircle(colors[idx])
    }
}

object Actions {

    fun toast(ctx: Context, msg: String) {
        Toast.makeText(ctx, msg, Toast.LENGTH_SHORT).show()
    }

    fun safeStart(ctx: Context, intent: Intent) {
        try {
            if (ctx !is Activity) intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            ctx.startActivity(intent)
        } catch (e: Exception) {
            toast(ctx, "No app found to do this")
        }
    }

    fun call(ctx: Context, number: String) {
        val uri = Uri.parse("tel:" + Uri.encode(number))
        val granted = ContextCompat.checkSelfPermission(ctx, Manifest.permission.CALL_PHONE) ==
            PackageManager.PERMISSION_GRANTED
        safeStart(ctx, Intent(if (granted) Intent.ACTION_CALL else Intent.ACTION_DIAL, uri))
    }

    fun sms(ctx: Context, number: String) {
        safeStart(ctx, Intent(Intent.ACTION_SENDTO, Uri.parse("smsto:" + Uri.encode(number))))
    }

    fun email(ctx: Context, address: String) {
        val i = Intent(Intent.ACTION_SENDTO, Uri.parse("mailto:" + address))
        safeStart(ctx, Intent.createChooser(i, "Send email"))
    }

    fun international(ctx: Context, number: String): String {
        val trimmed = number.trim()
        val d = trimmed.filter { it.isDigit() }
        if (trimmed.startsWith("+")) return d
        if (d.startsWith("00")) return d.substring(2)
        val cc = Prefs.countryCode(ctx).filter { it.isDigit() }
        if (cc.isEmpty()) return d
        if (d.startsWith("0")) return cc + d.substring(1)
        if (d.startsWith(cc)) return d
        return cc + d
    }

    fun copy(ctx: Context, text: String) {
        val cm = ctx.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        cm.setPrimaryClip(ClipData.newPlainText("number", text))
    }

    fun isInstalled(ctx: Context, app: SocialApp): Boolean =
        ctx.packageManager.getLaunchIntentForPackage(app.pkg) != null

    fun openSocial(ctx: Context, app: SocialApp, number: String) {
        val launch = ctx.packageManager.getLaunchIntentForPackage(app.pkg)
        if (launch == null) {
            toast(ctx, app.label + " is not installed")
            try {
                safeStartRaw(ctx, Intent(Intent.ACTION_VIEW, Uri.parse("market://details?id=" + app.pkg)))
            } catch (e: Exception) {
                safeStart(
                    ctx,
                    Intent(Intent.ACTION_VIEW, Uri.parse("https://play.google.com/store/apps/details?id=" + app.pkg))
                )
            }
            return
        }
        val link = app.link
        if (link != null) {
            try {
                val i = Intent(Intent.ACTION_VIEW, Uri.parse(link(international(ctx, number))))
                i.setPackage(app.pkg)
                safeStartRaw(ctx, i)
                return
            } catch (e: Exception) {
                // fall through to copy
            }
        }
        copy(ctx, number)
        toast(ctx, "Number copied - paste it in " + app.label + " search")
        safeStart(ctx, launch)
    }

    private fun safeStartRaw(ctx: Context, intent: Intent) {
        if (ctx !is Activity) intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        ctx.startActivity(intent)
    }

    fun withNumber(ctx: Context, contact: Contact, block: (String) -> Unit) {
        when (contact.phones.size) {
            0 -> toast(ctx, "No phone number")
            1 -> block(contact.phones[0].number)
            else -> {
                val labels = contact.phones.map { it.number + "  (" + it.type + ")" }.toTypedArray()
                AlertDialog.Builder(ctx)
                    .setTitle(contact.name)
                    .setItems(labels) { _, i -> block(contact.phones[i].number) }
                    .show()
            }
        }
    }

    fun withEmail(ctx: Context, contact: Contact, block: (String) -> Unit) {
        when (contact.emails.size) {
            0 -> toast(ctx, "No email address")
            1 -> block(contact.emails[0].address)
            else -> {
                val labels = contact.emails.map { it.address + "  (" + it.type + ")" }.toTypedArray()
                AlertDialog.Builder(ctx)
                    .setTitle(contact.name)
                    .setItems(labels) { _, i -> block(contact.emails[i].address) }
                    .show()
            }
        }
    }

    fun toggleStar(ctx: Context, contact: Contact) {
        val values = ContentValues()
        values.put(ContactsContract.Contacts.STARRED, if (contact.starred) 0 else 1)
        try {
            ctx.contentResolver.update(
                ContentUris.withAppendedId(ContactsContract.Contacts.CONTENT_URI, contact.id),
                values, null, null
            )
        } catch (e: Exception) {
            toast(ctx, "Could not update favorite")
        }
    }

    fun edit(ctx: Context, contact: Contact) {
        val uri = ContactsContract.Contacts.getLookupUri(contact.id, contact.lookupKey)
        val i = Intent(Intent.ACTION_EDIT)
        i.setDataAndType(uri, ContactsContract.Contacts.CONTENT_ITEM_TYPE)
        i.putExtra("finishActivityOnSaveCompleted", true)
        safeStart(ctx, i)
    }

    fun create(ctx: Context, phone: String? = null) {
        val i = Intent(Intent.ACTION_INSERT, ContactsContract.Contacts.CONTENT_URI)
        if (phone != null) i.putExtra(ContactsContract.Intents.Insert.PHONE, phone)
        safeStart(ctx, i)
    }

    fun confirmDelete(ctx: Context, contact: Contact, onDone: () -> Unit) {
        AlertDialog.Builder(ctx)
            .setTitle("Delete contact")
            .setMessage("Delete " + contact.name + " permanently?")
            .setNegativeButton("Cancel", null)
            .setPositiveButton("Delete") { _, _ ->
                try {
                    ctx.contentResolver.delete(
                        ContentUris.withAppendedId(ContactsContract.Contacts.CONTENT_URI, contact.id),
                        null, null
                    )
                    toast(ctx, "Deleted")
                    onDone()
                } catch (e: Exception) {
                    toast(ctx, "Could not delete contact")
                }
            }
            .show()
    }
}
