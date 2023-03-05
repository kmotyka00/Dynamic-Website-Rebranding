import { ResponsiveChoropleth } from '@nivo/geo';
import { tokens } from '../theme';
import { useTheme } from '@mui/material';
import { geoFeatures } from '../data/mockGeoFeatures';
import { mockGeographyData } from '../data/mockData';

const GeoChart = ({isDashboard = false}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    return (
        <ResponsiveChoropleth
        data={mockGeographyData}
        theme={
            {
                axis: {
                    domain: {
                        line: {
                            stroke: colors.grey[100]
                        }
                    },
                    legend: {
                        text: {
                            fill: colors.grey[100]
                        }
                    },
                    ticks: {
                        line: {
                            stroke: colors.grey[100],
                            strokeWidth: 1,
                        }
                    }
                },
                legends: {
                    text: {
                        fill: colors.grey[100],
                    }
                }
            }
        }
        features={geoFeatures.features}
        margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
        domain={[ 0, 1000000 ]}
        projectionScale={isDashboard ? 50 : 150}
        unknownColor="#666666"
        label="properties.name"
        valueFormat=".2s"
        projectionTranslation={isDashboard ? [0.49, 0.46] : [ 0.5, 0.5 ]}
        projectionRotation={[ 0, 0, 0 ]}
        borderWidth={1.5}
        borderColor="#fff"
        legends={isDashboard ? undefined : [
            {
                anchor: 'bottom-left',
                direction: 'column',
                justify: true,
                translateX: 20,
                translateY: -100,
                itemsSpacing: 0,
                itemWidth: 94,
                itemHeight: 18,
                itemDirection: 'left-to-right',
                itemTextColor: colors.grey[100],
                itemOpacity: 0.85,
                symbolSize: 18,
                effects: [
                    {
                        on: 'hover',
                        style: {
                            itemTextColor: '#fff',
                            itemOpacity: 1
                        }
                    }
                ]
            }
        ]}
    />
    )
}

export default GeoChart;