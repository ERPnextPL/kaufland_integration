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
# after_install = "kaufland_integration.kaufland_integration.scheduler.after_install.install"

# Uninstallation
# ------------

# before_uninstall = "kaufland_integration.uninstall.before_uninstall"
after_uninstall = "kaufland_integration.kaufland_integration.scheduler.after_uninstall.uninstall"

scheduler_events = {
	# "all": [
	# 	"kaufland_integration.scheduler.kaufland.test"
	#  ],
	# "daily": [
	# 	"symfonia_integration.tasks.daily"
	# ],
	"hourly": [
		"kaufland_integration.kaufland_integration.scheduler.kaufland.get_orders"
	],
	# "weekly": [
	# 	"symfonia_integration.tasks.weekly"
	# ],
	# "monthly": [
	# 	"symfonia_integration.tasks.monthly"
	# ],
}