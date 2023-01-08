
import React from 'react';
import { useEffect, useContext } from 'react'
import Plotly from 'plotly.js-dist-min'

import { TickerContext } from '../../contexts/TickerContextProvider';

function Increase() {

    const { initValue, currentValue } = useContext(TickerContext);

    useEffect(() => {

        var data = [
            {
                type: "indicator",
                mode: "number+delta",
                value: currentValue,
                domain: { row: 0, column: 1 }
            },
        ]; 

        var layout = {
            plot_bgcolor: "#3A3B3C",
            paper_bgcolor: "#18191A",
            template: {
                data: {
                    indicator: [
                        {
                            title: { text: "Price" },
                            delta: { reference: initValue }
                        }
                    ]
                }
            }
        };

        Plotly.newPlot('Increase', data, layout);
    }, [currentValue, initValue])

    return (
        <div>
            <div id="Increase" ></div>
        </div>
    );

}

export default Increase;