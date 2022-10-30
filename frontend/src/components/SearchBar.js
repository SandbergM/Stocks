import { useEffect } from "react";

export default function SearchBar() {

    const loadData = async () => {
        let companyNameSearch = "ava";
        let res = await fetch(`/ticker/ticker_search?company_name_search=${companyNameSearch}`)
        try {
            res = await res.json()
            console.log(res);
        } catch {
            console.log("Bad stuff");
        }
    }

    useEffect(() => {
        loadData()
    }, [])

    return (<></>)
}