import os

PROJECT_ROOT = "."

FILES = {
    "build.gradle.kts": """
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
}
""",

    "gradle.properties": """
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
""",

    "settings.gradle.kts": """
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "FastContacts"
include(":app")
""",

    "gradle/libs.versions.toml": """
[versions]
agp = "8.7.3"
kotlin = "2.0.21"
coreKt = "1.15.0"
appcompat = "1.7.0"
material = "1.12.0"
recyclerview = "1.3.2"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKt" }
androidx-appcompat = { group = "androidx.appcompat", name = "appcompat", version.ref = "appcompat" }
material = { group = "com.google.android.material", name = "material", version.ref = "material" }
androidx-recyclerview = { group = "androidx.recyclerview", name = "recyclerview", version.ref = "recyclerview" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
""",

    "app/proguard-rules.pro": """
# ProGuard rules for Fast Contacts
""",

    "app/build.gradle.kts": """
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "com.example.fastcontacts"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.fastcontacts"
        minSdk = 24
        targetSdk = 35
        versionCode = 2
        versionName = "2.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
    implementation(libs.androidx.recyclerview)
}
""",

    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.READ_CONTACTS" />
    <uses-permission android:name="android.permission.WRITE_CONTACTS" />
    <uses-permission android:name="android.permission.CALL_PHONE" />

    <queries>
        <package android:name="com.whatsapp" />
        <package android:name="com.whatsapp.w4b" />
        <package android:name="org.telegram.messenger" />
        <package android:name="com.viber.voip" />
        <package android:name="com.imo.android.imoim" />
        <package android:name="org.thoughtcrime.securesms" />
        <package android:name="com.facebook.orca" />
        <package android:name="com.facebook.katana" />
        <package android:name="com.instagram.android" />
        <package android:name="com.skype.raider" />
        <package android:name="com.snapchat.android" />
        <package android:name="com.google.android.apps.tachyon" />
        <intent>
            <action android:name="android.intent.action.VIEW" />
            <data android:scheme="https" />
        </intent>
        <intent>
            <action android:name="android.intent.action.SENDTO" />
            <data android:scheme="mailto" />
        </intent>
        <intent>
            <action android:name="android.intent.action.SENDTO" />
            <data android:scheme="smsto" />
        </intent>
    </queries>

    <application
        android:allowBackup="true"
        android:icon="@android:drawable/sym_def_app_icon"
        android:label="Fast Contacts"
        android:supportsRtl="true"
        android:theme="@style/Theme.FastContacts">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:windowSoftInputMode="adjustPan">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity android:name=".DetailActivity" />
        <activity android:name=".DialpadActivity" />
        <activity android:name=".SettingsActivity" />

    </application>
</manifest>
""",

    "app/src/main/res/values/themes.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.FastContacts" parent="Theme.Material3.DayNight.NoActionBar">
        <item name="colorPrimary">#0B57D0</item>
        <item name="colorOnPrimary">#FFFFFF</item>
        <item name="colorPrimaryContainer">#D3E3FD</item>
        <item name="colorOnPrimaryContainer">#041E49</item>
        <item name="colorSecondaryContainer">#E1E2EC</item>
        <item name="colorOnSecondaryContainer">#191C20</item>
        <item name="android:colorBackground">#F8F9FA</item>
        <item name="colorSurface">#FFFFFF</item>
        <item name="colorOnSurface">#1F1F1F</item>
        <item name="colorSurfaceVariant">#E1E3E1</item>
        <item name="colorOnSurfaceVariant">#444746</item>
    </style>
</resources>
""",

    "app/src/main/res/layout/activity_main.xml": """<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fitsSystemWindows="true">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical">

        <com.google.android.material.card.MaterialCardView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginHorizontal="16dp"
            android:layout_marginTop="12dp"
            android:layout_marginBottom="8dp"
            app:cardCornerRadius="28dp"
            app:cardElevation="2dp"
            app:cardBackgroundColor="?attr/colorSecondaryContainer"
            app:strokeWidth="0dp">

            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="56dp"
                android:gravity="center_vertical"
                android:orientation="horizontal"
                android:paddingHorizontal="16dp">

                <ImageView
                    android:layout_width="24dp"
                    android:layout_height="24dp"
                    android:src="@android:drawable/ic_menu_search"
                    app:tint="?attr/colorOnSecondaryContainer" />

                <EditText
                    android:id="@+id/search"
                    android:layout_width="0dp"
                    android:layout_height="match_parent"
                    android:layout_weight="1"
                    android:background="@null"
                    android:hint="Search contacts..."
                    android:imeOptions="actionSearch"
                    android:inputType="textPersonName"
                    android:paddingHorizontal="12dp"
                    android:textColor="?attr/colorOnSecondaryContainer"
                    android:textColorHint="?attr/colorOnSurfaceVariant"
                    android:textSize="16sp" />

                <ImageButton
                    android:id="@+id/btnClearSearch"
                    android:layout_width="40dp"
                    android:layout_height="40dp"
                    android:background="?attr/selectableItemBackgroundBorderless"
                    android:contentDescription="Clear search"
                    android:src="@android:drawable/ic_menu_close_clear_cancel"
                    android:visibility="gone"
                    app:tint="?attr/colorOnSecondaryContainer" />

                <ImageButton
                    android:id="@+id/btnSettings"
                    android:layout_width="40dp"
                    android:layout_height="40dp"
                    android:background="?attr/selectableItemBackgroundBorderless"
                    android:contentDescription="Settings"
                    android:src="@android:drawable/ic_menu_preferences"
                    app:tint="?attr/colorOnSecondaryContainer" />
            </LinearLayout>
        </com.google.android.material.card.MaterialCardView>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:gravity="center_vertical"
            android:orientation="horizontal"
            android:paddingHorizontal="16dp"
            android:paddingVertical="4dp">

            <com.google.android.material.button.MaterialButtonToggleGroup
                android:id="@+id/toggleGroup"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                app:singleSelection="true"
                app:selectionRequired="true">

                <Button
                    android:id="@+id/btnAll"
                    style="@style/Widget.Material3.Button.OutlinedButton"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="All" />

                <Button
                    android:id="@+id/btnFavorites"
                    style="@style/Widget.Material3.Button.OutlinedButton"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="Favorites" />
            </com.google.android.material.button.MaterialButtonToggleGroup>

            <TextView
                android:id="@+id/tvCount"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:gravity="end"
                android:textColor="?attr/colorOnSurfaceVariant"
                android:textSize="13sp" />
        </LinearLayout>

        <FrameLayout
            android:layout_width="match_parent"
            android:layout_height="0dp"
            android:layout_weight="1">

            <androidx.recyclerview.widget.RecyclerView
                android:id="@+id/list"
                android:layout_width="match_parent"
                android:layout_height="match_parent"
                android:clipToPadding="false"
                android:paddingBottom="88dp" />

            <LinearLayout
                android:id="@+id/emptyState"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_gravity="center"
                android:gravity="center"
                android:orientation="vertical"
                android:padding="24dp"
                android:visibility="gone">

                <ImageView
                    android:layout_width="64dp"
                    android:layout_height="64dp"
                    android:alpha="0.4"
                    android:src="@android:drawable/ic_menu_search"
                    app:tint="?attr/colorOnSurfaceVariant" />

                <TextView
                    android:id="@+id/emptyTitle"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_marginTop="12dp"
                    android:text="No contacts found"
                    android:textColor="?attr/colorOnSurface"
                    android:textSize="18sp"
                    android:textStyle="bold" />

                <TextView
                    android:id="@+id/emptySubtitle"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_marginTop="4dp"
                    android:text="Try adjusting your search query"
                    android:textColor="?attr/colorOnSurfaceVariant"
                    android:textSize="14sp" />
            </LinearLayout>

            <com.google.android.material.card.MaterialCardView
                android:id="@+id/permissionPanel"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_gravity="center"
                android:layout_margin="24dp"
                android:visibility="gone"
                app:cardCornerRadius="16dp"
                app:cardElevation="4dp">

                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:gravity="center"
                    android:orientation="vertical"
                    android:padding="24dp">

                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Permission Required"
                        android:textColor="?attr/colorOnSurface"
                        android:textSize="20sp"
                        android:textStyle="bold" />

                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:layout_marginTop="8dp"
                        android:gravity="center"
                        android:text="Fast Contacts requires access to your device contacts to render, search, and manage your phonebook directly."
                        android:textColor="?attr/colorOnSurfaceVariant"
                        android:textSize="14sp" />

                    <Button
                        android:id="@+id/permissionButton"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:layout_marginTop="16dp"
                        android:text="Grant Access" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>
        </FrameLayout>
    </LinearLayout>

    <com.google.android.material.floatingactionbutton.FloatingActionButton
        android:id="@+id/fabDialpad"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom|end"
        android:layout_margin="16dp"
        android:contentDescription="Open Dialpad"
        android:src="@android:drawable/ic_menu_call"
        app:containerColor="?attr/colorPrimaryContainer"
        app:tint="?attr/colorOnPrimaryContainer" />
</androidx.coordinatorlayout.widget.CoordinatorLayout>
""",

    "app/src/main/res/layout/item_header.xml": """<?xml version="1.0" encoding="utf-8"?>
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/headerText"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:paddingStart="20dp"
    android:paddingTop="16dp"
    android:paddingEnd="16dp"
    android:paddingBottom="6dp"
    android:textColor="?attr/colorPrimary"
    android:textSize="14sp"
    android:textStyle="bold" />
""",

    "app/src/main/res/layout/item_contact.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:background="?attr/selectableItemBackground"
    android:gravity="center_vertical"
    android:orientation="horizontal"
    android:paddingHorizontal="16dp"
    android:paddingVertical="10dp">

    <TextView
        android:id="@+id/avatar"
        android:layout_width="44dp"
        android:layout_height="44dp"
        android:gravity="center"
        android:textColor="#FFFFFF"
        android:textSize="18sp"
        android:textStyle="bold" />

    <LinearLayout
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginStart="16dp"
        android:layout_weight="1"
        android:orientation="vertical">

        <TextView
            android:id="@+id/name"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textColor="?attr/colorOnSurface"
            android:textSize="16sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/number"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="2dp"
            android:textColor="?attr/colorOnSurfaceVariant"
            android:textSize="14sp" />

        <TextView
            android:id="@+id/email"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="2dp"
            android:textColor="?attr/colorOnSurfaceVariant"
            android:textSize="12sp"
            android:visibility="gone" />
    </LinearLayout>

    <ImageButton
        android:id="@+id/btnFav"
        android:layout_width="40dp"
        android:layout_height="40dp"
        android:background="?attr/selectableItemBackgroundBorderless"
        android:contentDescription="Favorite"
        android:src="@android:drawable/btn_star_big_off" />

    <ImageButton
        android:id="@+id/btnSms"
        android:layout_width="40dp"
        android:layout_height="40dp"
        android:background="?attr/selectableItemBackgroundBorderless"
        android:contentDescription="SMS"
        android:src="@android:drawable/sym_action_chat" />

    <ImageButton
        android:id="@+id/btnCall"
        android:layout_width="40dp"
        android:layout_height="40dp"
        android:background="?attr/selectableItemBackgroundBorderless"
        android:contentDescription="Call"
        android:src="@android:drawable/ic_menu_call" />
</LinearLayout>
""",

    "app/src/main/res/layout/row_phone.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:gravity="center_vertical"
    android:orientation="horizontal"
    android:paddingVertical="10dp">

    <LinearLayout
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_weight="1"
        android:orientation="vertical">

        <TextView
            android:id="@+id/rowNumber"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textColor="?attr/colorOnSurface"
            android:textSize="16sp" />

        <TextView
            android:id="@+id/rowType"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="2dp"
            android:textColor="?attr/colorOnSurfaceVariant"
            android:textSize="12sp" />
    </LinearLayout>

    <TextView
        android:id="@+id/rowWa"
        android:layout_width="36dp"
        android:layout_height="36dp"
        android:layout_marginEnd="8dp"
        android:gravity="center"
        android:text="WA"
        android:textColor="#FFFFFF"
        android:textSize="12sp"
        android:textStyle="bold" />

    <ImageButton
        android:id="@+id/rowSms"
        android:layout_width="40dp"
        android:layout_height="40dp"
        android:background="?attr/selectableItemBackgroundBorderless"
        android:contentDescription="SMS"
        android:src="@android:drawable/sym_action_chat" />

    <ImageButton
        android:id="@+id/rowCall"
        android:layout_width="40dp"
        android:layout_height="40dp"
        android:background="?attr/selectableItemBackgroundBorderless"
        android:contentDescription="Call"
        android:src="@android:drawable/ic_menu_call" />
</LinearLayout>
""",

    "app/src/main/res/layout/row_email.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:background="?attr/selectableItemBackground"
    android:orientation="vertical"
    android:paddingVertical="10dp">

    <TextView
        android:id="@+id/emailAddr"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:textColor="?attr/colorPrimary"
        android:textSize="16sp" />

    <TextView
        android:id="@+id/emailType"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="2dp"
        android:textColor="?attr/colorOnSurfaceVariant"
        android:textSize="12sp" />
</LinearLayout>
""",

    "app/src/main/res/layout/activity_detail.xml": """<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fitsSystemWindows="true">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:gravity="center_horizontal"
        android:orientation="vertical"
        android:padding="24dp">

        <TextView
            android:id="@+id/detailAvatar"
            android:layout_width="88dp"
            android:layout_height="88dp"
            android:gravity="center"
            android:textColor="#FFFFFF"
            android:textSize="36sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/detailName"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="16dp"
            android:textColor="?attr/colorOnSurface"
            android:textSize="22sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/detailPhone"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="6dp"
            android:textColor="?attr/colorOnSurfaceVariant"
            android:textSize="15sp" />

        <TextView
            android:id="@+id/detailEmail"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="4dp"
            android:textColor="?attr/colorPrimary"
            android:textSize="14sp" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="20dp"
            android:gravity="center"
            android:orientation="vertical">

            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal">

                <Button
                    android:id="@+id/btnCallAction"
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_marginEnd="4dp"
                    android:layout_weight="1"
                    android:text="Call" />

                <Button
                    android:id="@+id/btnSmsAction"
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_marginEnd="4dp"
                    android:layout_weight="1"
                    android:text="SMS" />

                <Button
                    android:id="@+id/btnWhatsAppAction"
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:text="WhatsApp" />
            </LinearLayout>

            <Button
                android:id="@+id/btnEmailAction"
                style="@style/Widget.Material3.Button.OutlinedButton"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="8dp"
                android:text="Send Email" />
        </LinearLayout>

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="24dp"
            android:text="Phone numbers"
            android:textColor="?attr/colorPrimary"
            android:textSize="14sp"
            android:textStyle="bold" />

        <LinearLayout
            android:id="@+id/phonesContainer"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical" />

        <TextView
            android:id="@+id/emailsTitle"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="16dp"
            android:text="Emails"
            android:textColor="?attr/colorPrimary"
            android:textSize="14sp"
            android:textStyle="bold" />

        <LinearLayout
            android:id="@+id/emailsContainer"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical" />

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="16dp"
            android:text="Chat and social apps"
            android:textColor="?attr/colorPrimary"
            android:textSize="14sp"
            android:textStyle="bold" />

        <GridLayout
            android:id="@+id/socialGrid"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:columnCount="4" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="24dp"
            android:orientation="horizontal">

            <Button
                android:id="@+id/btnFavAction"
                style="@style/Widget.Material3.Button.OutlinedButton"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_marginEnd="4dp"
                android:layout_weight="1"
                android:text="Favorite" />

            <Button
                android:id="@+id/btnEditAction"
                style="@style/Widget.Material3.Button.OutlinedButton"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_marginEnd="4dp"
                android:layout_weight="1"
                android:text="Edit" />

            <Button
                android:id="@+id/btnDeleteAction"
                style="@style/Widget.Material3.Button.OutlinedButton"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="Delete" />
        </LinearLayout>
    </LinearLayout>
</ScrollView>
""",

    "app/src/main/res/layout/activity_dialpad.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fitsSystemWindows="true"
    android:orientation="vertical">

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/suggestions"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1" />

    <TextView
        android:id="@+id/dialDisplay"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:minHeight="64dp"
        android:padding="12dp"
        android:textColor="?attr/colorOnSurface"
        android:textSize="32sp" />

    <GridLayout
        android:id="@+id/keypad"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:columnCount="3"
        android:padding="8dp" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="8dp">

        <Button
            android:id="@+id/btnAddContact"
            style="@style/Widget.Material3.Button.OutlinedButton"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_marginEnd="4dp"
            android:layout_weight="1"
            android:text="Save" />

        <Button
            android:id="@+id/btnDialCall"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_marginEnd="4dp"
            android:layout_weight="2"
            android:text="Call" />

        <Button
            android:id="@+id/btnBackspace"
            style="@style/Widget.Material3.Button.OutlinedButton"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Del" />
    </LinearLayout>
</LinearLayout>
""",

    "app/src/main/res/layout/activity_settings.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fitsSystemWindows="true"
    android:orientation="vertical"
    android:padding="20dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginBottom="20dp"
        android:text="Contacts Settings"
        android:textColor="?attr/colorOnSurface"
        android:textSize="22sp"
        android:textStyle="bold" />

    <CheckBox
        android:id="@+id/chkShowEmail"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:checked="true"
        android:text="Show Email in Contact List" />

    <CheckBox
        android:id="@+id/chkSortLast"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Sort list by last name" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="20dp"
        android:text="Default country code for messaging apps (e.g., 880)"
        android:textColor="?attr/colorOnSurfaceVariant"
        android:textSize="13sp" />

    <EditText
        android:id="@+id/etCountryCode"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Country code"
        android:inputType="number"
        android:maxLength="4" />

    <Button
        android:id="@+id/btnSyncSettings"
        style="@style/Widget.Material3.Button.OutlinedButton"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="28dp"
        android:text="Google / Account Sync Settings" />

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:text="Privacy Guarantee: Fast Contacts contains no internet permission, ads, login requirement, or analytics tracking. All contacts remain in Android system storage."
        android:textColor="?attr/colorOnSurfaceVariant"
        android:textSize="12sp" />
</LinearLayout>
""",

    "app/src/main/java/com/example/fastcontacts/Contact.kt": """package com.example.fastcontacts

data class Phone(val number: String, val type: String)
data class Email(val address: String, val type: String)

data class Contact(
    val id: Long,
    val name: String,
    val firstName: String,
    val lastName: String,
    val phones: List<Phone> = emptyList(),
    val emails: List<Email> = emptyList(),
    val starred: Boolean = false,
    val lookupKey: String = ""
)
""",

    "app/src/main/java/com/example/fastcontacts/Prefs.kt": """package com.example.fastcontacts

import android.content.Context

object Prefs {
    private fun sp(c: Context) = c.getSharedPreferences("fast_contacts_prefs", Context.MODE_PRIVATE)

    fun showEmail(c: Context): Boolean = sp(c).getBoolean("show_email", true)
    fun setShowEmail(c: Context, v: Boolean) = sp(c).edit().putBoolean("show_email", v).apply()

    fun sortByLast(c: Context): Boolean = sp(c).getBoolean("sort_last", false)
    fun setSortByLast(c: Context, v: Boolean) = sp(c).edit().putBoolean("sort_last", v).apply()

    fun countryCode(c: Context): String = sp(c).getString("country_code", "") ?: ""
    fun setCountryCode(c: Context, v: String) = sp(c).edit().putString("country_code", v).apply()
}
""",

    "app/src/main/java/com/example/fastcontacts/ContactsRepository.kt": """package com.example.fastcontacts

import android.content.Context
import android.provider.ContactsContract

object ContactsRepository {

    fun loadAll(context: Context): List<Contact> = load(context, null)

    fun loadById(context: Context, id: Long): Contact? = load(context, id).firstOrNull()

    private fun load(context: Context, onlyId: Long?): List<Contact> {
        val contactsMap = LinkedHashMap<Long, MutableContact>()
        val cr = context.contentResolver

        val cSel = if (onlyId != null) "${ContactsContract.Contacts._ID}=?" else null
        val cArgs = if (onlyId != null) arrayOf(onlyId.toString()) else null

        val cursor = cr.query(
            ContactsContract.Contacts.CONTENT_URI,
            arrayOf(
                ContactsContract.Contacts._ID,
                ContactsContract.Contacts.DISPLAY_NAME_PRIMARY,
                ContactsContract.Contacts.STARRED,
                ContactsContract.Contacts.LOOKUP_KEY
            ),
            cSel, cArgs, "${ContactsContract.Contacts.DISPLAY_NAME_PRIMARY} ASC"
        )

        cursor?.use {
            val idIdx = it.getColumnIndex(ContactsContract.Contacts._ID)
            val nameIdx = it.getColumnIndex(ContactsContract.Contacts.DISPLAY_NAME_PRIMARY)
            val starIdx = it.getColumnIndex(ContactsContract.Contacts.STARRED)
            val lookupIdx = it.getColumnIndex(ContactsContract.Contacts.LOOKUP_KEY)
            while (it.moveToNext()) {
                val id = it.getLong(idIdx)
                val name = it.getString(nameIdx) ?: "Unknown"
                val starred = it.getInt(starIdx) == 1
                val lookup = it.getString(lookupIdx) ?: ""
                contactsMap[id] = MutableContact(id, name, starred, lookup)
            }
        }

        if (contactsMap.isEmpty()) return emptyList()

        val nameMap = HashMap<Long, Pair<String, String>>()
        val nameSel = if (onlyId != null) {
            "${ContactsContract.Data.MIMETYPE}=? AND ${ContactsContract.Data.CONTACT_ID}=?"
        } else {
            "${ContactsContract.Data.MIMETYPE}=?"
        }
        val nameArgs = if (onlyId != null) {
            arrayOf(ContactsContract.CommonDataKinds.StructuredName.CONTENT_ITEM_TYPE, onlyId.toString())
        } else {
            arrayOf(ContactsContract.CommonDataKinds.StructuredName.CONTENT_ITEM_TYPE)
        }

        val nameCursor = cr.query(
            ContactsContract.Data.CONTENT_URI,
            arrayOf(
                ContactsContract.Data.CONTACT_ID,
                ContactsContract.CommonDataKinds.StructuredName.GIVEN_NAME,
                ContactsContract.CommonDataKinds.StructuredName.FAMILY_NAME
            ),
            nameSel, nameArgs, null
        )

        nameCursor?.use {
            val cIdIdx = it.getColumnIndex(ContactsContract.Data.CONTACT_ID)
            val givenIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.StructuredName.GIVEN_NAME)
            val familyIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.StructuredName.FAMILY_NAME)
            while (it.moveToNext()) {
                val cId = it.getLong(cIdIdx)
                val given = it.getString(givenIdx) ?: ""
                val family = it.getString(familyIdx) ?: ""
                if (!nameMap.containsKey(cId) || (given.isNotBlank() || family.isNotBlank())) {
                    nameMap[cId] = Pair(given, family)
                }
            }
        }

        nameMap.forEach { (cId, pair) ->
            contactsMap[cId]?.let {
                it.firstName = pair.first
                it.lastName = pair.second
            }
        }

        val pSel = if (onlyId != null) "${ContactsContract.CommonDataKinds.Phone.CONTACT_ID}=?" else null
        val phoneCursor = cr.query(
            ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
            arrayOf(
                ContactsContract.CommonDataKinds.Phone.CONTACT_ID,
                ContactsContract.CommonDataKinds.Phone.NUMBER,
                ContactsContract.CommonDataKinds.Phone.TYPE,
                ContactsContract.CommonDataKinds.Phone.LABEL
            ),
            pSel, cArgs, null
        )

        phoneCursor?.use {
            val cIdIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Phone.CONTACT_ID)
            val numIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER)
            val typeIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Phone.TYPE)
            val labelIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Phone.LABEL)
            while (it.moveToNext()) {
                val cId = it.getLong(cIdIdx)
                val num = it.getString(numIdx) ?: continue
                val typeInt = it.getInt(typeIdx)
                val custom = it.getString(labelIdx) ?: ""
                val typeLabel = ContactsContract.CommonDataKinds.Phone.getTypeLabel(
                    context.resources, typeInt, custom
                ).toString()
                contactsMap[cId]?.addPhone(Phone(num, typeLabel))
            }
        }

        val eSel = if (onlyId != null) "${ContactsContract.CommonDataKinds.Email.CONTACT_ID}=?" else null
        val emailCursor = cr.query(
            ContactsContract.CommonDataKinds.Email.CONTENT_URI,
            arrayOf(
                ContactsContract.CommonDataKinds.Email.CONTACT_ID,
                ContactsContract.CommonDataKinds.Email.ADDRESS,
                ContactsContract.CommonDataKinds.Email.TYPE,
                ContactsContract.CommonDataKinds.Email.LABEL
            ),
            eSel, cArgs, null
        )

        emailCursor?.use {
            val cIdIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Email.CONTACT_ID)
            val addrIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Email.ADDRESS)
            val typeIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Email.TYPE)
            val labelIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Email.LABEL)
            while (it.moveToNext()) {
                val cId = it.getLong(cIdIdx)
                val addr = it.getString(addrIdx) ?: continue
                val typeInt = it.getInt(typeIdx)
                val custom = it.getString(labelIdx) ?: ""
                val typeLabel = ContactsContract.CommonDataKinds.Email.getTypeLabel(
                    context.resources, typeInt, custom
                ).toString()
                contactsMap[cId]?.addEmail(Email(addr, typeLabel))
            }
        }

        return contactsMap.values.map { it.toContact() }
    }

    private class MutableContact(
        val id: Long,
        val name: String,
        val starred: Boolean,
        val lookupKey: String
    ) {
        var firstName: String = ""
        var lastName: String = ""
        val phones = mutableListOf<Phone>()
        val emails = mutableListOf<Email>()

        fun addPhone(p: Phone) {
            val digits = p.number.filter { it.isDigit() }
            if (phones.none { it.number.filter { c -> c.isDigit() } == digits }) {
                phones.add(p)
            }
        }

        fun addEmail(e: Email) {
            if (emails.none { it.address.equals(e.address, ignoreCase = true) }) {
                emails.add(e)
            }
        }

        fun toContact(): Contact {
            val effFirst = firstName.ifBlank { name.trim().split(" ").firstOrNull() ?: "" }
            val effLast = lastName.ifBlank {
                val parts = name.trim().split(" ")
                if (parts.size > 1) parts.last() else ""
            }
            return Contact(id, name, effFirst, effLast, phones, emails, starred, lookupKey)
        }
    }
}
""",

    "app/src/main/java/com/example/fastcontacts/SearchEngine.kt": """package com.example.fastcontacts

class SearchEngine(private val contacts: List<Contact>) {

    fun search(query: String): List<Contact> {
        val q = query.lowercase().trim()
        if (q.isBlank()) return contacts
        val qDigits = q.filter { it.isDigit() }

        val scored = ArrayList<Pair<Int, Contact>>()
        for (c in contacts) {
            val tier = calculateTier(c, q, qDigits)
            if (tier >= 0) {
                scored.add(Pair(tier, c))
            }
        }

        return scored
            .sortedWith(
                compareBy<Pair<Int, Contact>>(
                    { it.first },
                    { it.second.firstName.lowercase() },
                    { it.second.name.lowercase() }
                )
            )
            .map { it.second }
    }

    private fun calculateTier(c: Contact, q: String, qDigits: String): Int {
        val first = c.firstName.lowercase().trim()
        val last = c.lastName.lowercase().trim()
        val full = c.name.lowercase().trim()

        return when {
            first == q -> 0
            first.startsWith(q) -> 1
            first.contains(q) -> 2
            last.isNotEmpty() && last.startsWith(q) -> 3
            full.startsWith(q) -> 4
            full.contains(q) -> 5
            qDigits.isNotEmpty() && c.phones.any { p ->
                p.number.filter { it.isDigit() }.contains(qDigits)
            } -> 6
            c.emails.any { it.address.lowercase().contains(q) } -> 7
            else -> -1
        }
    }

    companion object {
        fun sorted(list: List<Contact>, byLast: Boolean): List<Contact> {
            return list.sortedWith(compareBy(
                { key(it, byLast) },
                { it.name.lowercase() }
            ))
        }

        private fun key(c: Contact, byLast: Boolean): String {
            return if (byLast) {
                val primary = c.lastName.ifBlank { c.firstName }
                (primary + " " + c.firstName).lowercase()
            } else {
                c.name.lowercase()
            }
        }

        fun letterOf(c: Contact, byLast: Boolean): String {
            val k = key(c, byLast).trim()
            val ch = k.firstOrNull() ?: return "#"
            return if (ch.isLetter()) ch.uppercase() else "#"
        }
    }
}
""",

    "app/src/main/java/com/example/fastcontacts/Actions.kt": """package com.example.fastcontacts

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
""",

    "app/src/main/java/com/example/fastcontacts/ContactAdapter.kt": """package com.example.fastcontacts

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
""",

    "app/src/main/java/com/example/fastcontacts/MainActivity.kt": """package com.example.fastcontacts

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
""",

    "app/src/main/java/com/example/fastcontacts/DetailActivity.kt": """package com.example.fastcontacts

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
""",

    "app/src/main/java/com/example/fastcontacts/DialpadActivity.kt": """package com.example.fastcontacts

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.GridLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton

class DialpadActivity : AppCompatActivity() {

    private val number = StringBuilder()
    private lateinit var display: TextView
    private lateinit var adapter: ContactAdapter
    private var engine = SearchEngine(emptyList())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dialpad)

        display = findViewById(R.id.dialDisplay)

        adapter = ContactAdapter(
            onClick = { c ->
                val i = Intent(this, DetailActivity::class.java)
                i.putExtra("contact_id", c.id)
                startActivity(i)
            },
            onCallClick = { c -> Actions.withNumber(this, c) { n -> Actions.call(this, n) } },
            onSmsClick = { c -> Actions.withNumber(this, c) { n -> Actions.sms(this, n) } }
        )
        val suggestions = findViewById<RecyclerView>(R.id.suggestions)
        suggestions.layoutManager = LinearLayoutManager(this)
        suggestions.adapter = adapter

        buildKeypad()

        findViewById<Button>(R.id.btnDialCall).setOnClickListener {
            if (number.isNotEmpty()) Actions.call(this, number.toString())
        }
        findViewById<Button>(R.id.btnAddContact).setOnClickListener {
            if (number.isNotEmpty()) Actions.create(this, number.toString())
        }
        val back = findViewById<Button>(R.id.btnBackspace)
        back.setOnClickListener {
            if (number.isNotEmpty()) number.deleteCharAt(number.length - 1)
            refresh()
        }
        back.setOnLongClickListener {
            number.setLength(0)
            refresh()
            true
        }
        refresh()
    }

    override fun onResume() {
        super.onResume()
        Thread {
            val loaded = ContactsRepository.loadAll(this)
            runOnUiThread {
                engine = SearchEngine(SearchEngine.sorted(loaded, false))
                refresh()
            }
        }.start()
    }

    private fun dp(v: Int): Int = (v * resources.displayMetrics.density).toInt()

    private fun buildKeypad() {
        val keypad = findViewById<GridLayout>(R.id.keypad)
        val keys = listOf("1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#")
        for (k in keys) {
            val b = MaterialButton(this)
            b.text = k
            b.textSize = 24f
            val lp = GridLayout.LayoutParams(
                GridLayout.spec(GridLayout.UNDEFINED),
                GridLayout.spec(GridLayout.UNDEFINED, 1f)
            )
            lp.width = 0
            lp.height = dp(64)
            lp.setMargins(dp(4), dp(4), dp(4), dp(4))
            b.layoutParams = lp
            b.setOnClickListener {
                number.append(k)
                refresh()
            }
            if (k == "0") {
                b.setOnLongClickListener {
                    number.append("+")
                    refresh()
                    true
                }
            }
            keypad.addView(b)
        }
    }

    private fun refresh() {
        display.text = number.toString()
        if (number.isEmpty()) {
            adapter.submit(emptyList())
        } else {
            adapter.submit(engine.search(number.toString()).take(20))
        }
    }
}
""",

    "app/src/main/java/com/example/fastcontacts/SettingsActivity.kt": """package com.example.fastcontacts

import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.widget.Button
import android.widget.CheckBox
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import androidx.core.widget.doAfterTextChanged

class SettingsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)

        val chkEmail = findViewById<CheckBox>(R.id.chkShowEmail)
        chkEmail.isChecked = Prefs.showEmail(this)
        chkEmail.setOnCheckedChangeListener { _, checked ->
            Prefs.setShowEmail(this@SettingsActivity, checked)
        }

        val chkSort = findViewById<CheckBox>(R.id.chkSortLast)
        chkSort.isChecked = Prefs.sortByLast(this)
        chkSort.setOnCheckedChangeListener { _, checked ->
            Prefs.setSortByLast(this@SettingsActivity, checked)
        }

        val etCode = findViewById<EditText>(R.id.etCountryCode)
        etCode.setText(Prefs.countryCode(this))
        etCode.doAfterTextChanged {
            Prefs.setCountryCode(this@SettingsActivity, it?.toString() ?: "")
        }

        findViewById<Button>(R.id.btnSyncSettings).setOnClickListener {
            try {
                startActivity(Intent(Settings.ACTION_SYNC_SETTINGS))
            } catch (e: Exception) {
                startActivity(Intent(Settings.ACTION_SETTINGS))
            }
        }
    }
}
"""
}

def main():
    for rel_path, content in FILES.items():
        full_path = os.path.join(PROJECT_ROOT, rel_path.replace("/", os.sep))
        folder = os.path.dirname(full_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(full_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content.lstrip("\n"))
        print("Updated:", rel_path)
    print("\nComplete! Open the project in Android Studio and sync Gradle.")

if __name__ == "__main__":
    main()
