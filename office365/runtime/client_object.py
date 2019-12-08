class ClientObject(object):
    """Base client object"""

    def __init__(self, context, resource_path=None, properties=None):
        self._properties = {}
        self._metadata = {}
        if properties is not None:
            for k, v in properties.items():
                self.set_property(k, v, True)
        self._entity_type_name = None
        self._query_options = {}
        self._parent_collection = None
        self._context = context
        self._resource_path = resource_path
        self._resource_url = None

    def is_property_available(self, name):
        """Returns a Boolean value that indicates whether the specified property has been retrieved or set."""
        if name in self.properties and not (isinstance(self.properties[name], dict)
                                            and '__deferred' in self.properties[name]):
            return True
        return False

    def query_options_to_url(self):
        """Convert query options to url"""
        return '&'.join(['$%s=%s' % (key, value) for (key, value) in self.query_options.items()])

    def set_property(self, name, value, persist_changes=True):
        """Set resource property value"""
        self._metadata[name] = {'readonly': not persist_changes}
        self._properties[name] = value

    def expand(self, value):
        self.query_options['expand'] = value
        return self

    def select(self, value):
        self.query_options['select'] = value
        return self

    def remove_from_parent_collection(self):
        if self._parent_collection is None:
            return
        self._parent_collection.remove(self)

    def map_json(self, payload):
        self._properties = dict((k, v) for k, v in payload.items()
                                if k != '__metadata')

    @property
    def entityTypeName(self):
        if self._entity_type_name is None:
            self._entity_type_name = "SP." + type(self).__name__
        return self._entity_type_name

    @entityTypeName.setter
    def entityTypeName(self, value):
        self._entity_type_name = value

    @property
    def resourceUrl(self):
        """Get resource Url"""
        if self._resource_url:
            return self._resource_url
        elif self.resourcePath:
            self._resource_url = self.serviceRootUrl + self.resourcePath.build_path_url()
            if self.query_options:
                self._resource_url = self._resource_url + "?" + self.query_options_to_url()
        return self._resource_url

    @property
    def context(self):
        return self._context

    @property
    def serviceRootUrl(self):
        return self.context.serviceRootUrl

    @property
    def resourcePath(self):
        return self._resource_path

    @property
    def query_options(self):
        return self._query_options

    @property
    def typeName(self):
        return self.__module__ + "." + self.__class__.__name__

    @property
    def properties(self):
        return self._properties

    @property
    def metadata(self):
        return self._metadata
