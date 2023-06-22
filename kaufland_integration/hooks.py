from . import __version__ as app_version

app_name = "kaufland_integration"
app_title = "Kaufland Integration"
app_publisher = "ErpTech"
app_description = "Integration with Kaufland interface"
app_email = "maciej.miskiewicz@erptech.pl"
app_license = "MIT"

# Installation
# ------------

# before_install = "kaufland_integration.install.before_install"
after_install = "kaufland_integration.kaufland_integration.scheduler.after_install.install"

# Uninstallation
# ------------

# before_uninstall = "kaufland_integration.uninstall.before_uninstall"
after_uninstall = "kaufland_integration.kaufland_integration.scheduler.after_uninstall.uninstall"

# After sync
# ------------
after_sync = "kaufland_integration.kaufland_integration.scheduler.after_sync.update"

scheduler_events = {
	"hourly": [
		"kaufland_integration.kaufland_integration.scheduler.kaufland.get_orders"
	]
}

# Testing
# -------

before_tests = "kaufland_integration.kaufland_integration.tests.test_creditionals.beforeTestsCheckIfTherIsAConfiguration"
