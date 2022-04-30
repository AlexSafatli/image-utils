package main

import (
	"fmt"
	"github.com/evalphobia/go-config-loader"
	"os"
)

const (
	confType = "toml"
	basePath = "."
	apiKey   = "saucenao.api_key"
)

type configValues struct {
	ApiKey string
}

func loadConfigs() configValues {
	var conf *config.Config
	conf = config.NewConfig()
	if err := conf.LoadConfigs(basePath, confType); err != nil {
		_, _ = fmt.Fprintf(os.Stderr, "No %s config file in directory '%s'\n",
			confType, basePath)
		panic(err)
	}
	return configValues{
		ApiKey: conf.ValueString(apiKey),
	}
}
